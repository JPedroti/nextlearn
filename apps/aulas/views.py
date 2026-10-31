import time

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.contas.decorators import papel_requerido
from apps.turmas.models import Aluno, Turma

from .forms import AulaForm, QuestaoFormSet
from .models import Aula, Resposta
from .versoes import versao_para_aluno

# ---------------------------------------------------------------------------
# Professor
# ---------------------------------------------------------------------------


def _salvar_aula(form, formset):
    """Salva a aula e as questões, numerando-as na ordem em que aparecem no formulário."""
    with transaction.atomic():
        aula = form.save()
        formularios_validos = [f for f in formset.forms if f.cleaned_data]  # ignora questões extras em branco
        # Primeiro apaga as marcadas para excluir, para liberar os números de ordem.
        for f in formularios_validos:
            if f.cleaned_data.get("DELETE") and f.instance.pk:
                f.instance.delete()
        ordem = 1
        for f in formularios_validos:
            if f.cleaned_data.get("DELETE"):
                continue
            questao = f.save(commit=False)
            questao.aula = aula
            questao.ordem = ordem
            questao.save()
            ordem += 1
    return aula


@papel_requerido("professor")
def nova_aula(request, turma_pk):
    turma = get_object_or_404(Turma, pk=turma_pk, professor=request.user)
    form = AulaForm(request.POST or None, instance=Aula(turma=turma))
    formset = QuestaoFormSet(request.POST or None, instance=form.instance)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        aula = _salvar_aula(form, formset)
        messages.success(request, "Aula criada. Confira e publique quando quiser que os alunos vejam.")
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    return render(request, "aulas/form_aula.html", {"turma": turma, "form": form, "formset": formset})


@papel_requerido("professor")
def editar_aula(request, pk):
    aula = get_object_or_404(Aula, pk=pk, turma__professor=request.user)
    if aula.tem_respostas():
        # Mudar questões ou gabarito depois de respostas deixaria as correções antigas erradas.
        messages.error(request, "Esta aula já tem respostas de alunos e não pode mais ser editada.")
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    form = AulaForm(request.POST or None, instance=aula)
    formset = QuestaoFormSet(request.POST or None, instance=aula)
    if request.method == "POST" and form.is_valid() and formset.is_valid():
        _salvar_aula(form, formset)
        # Fatia 2: ao editar, apagar as VersaoAdaptada desta aula (o texto original mudou).
        messages.success(request, "Aula atualizada.")
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    return render(request, "aulas/form_aula.html", {"turma": aula.turma, "form": form, "formset": formset, "aula": aula})


@papel_requerido("professor")
def detalhe_professor(request, pk):
    aula = get_object_or_404(Aula.objects.select_related("turma"), pk=pk, turma__professor=request.user)
    alunos_que_responderam = Aluno.objects.filter(respostas__questao__aula=aula).distinct().count()
    contexto = {
        "aula": aula,
        "questoes": aula.questoes.all(),
        "alunos_que_responderam": alunos_que_responderam,
        "total_alunos": aula.turma.alunos.count(),
    }
    return render(request, "aulas/detalhe_professor.html", contexto)


@require_POST
@papel_requerido("professor")
def alternar_publicacao(request, pk):
    aula = get_object_or_404(Aula, pk=pk, turma__professor=request.user)
    aula.publicada = not aula.publicada
    aula.save(update_fields=["publicada"])
    if aula.publicada:
        messages.success(request, "Aula publicada: os alunos da turma já podem ver.")
    else:
        messages.success(request, "Aula despublicada: os alunos não veem mais esta aula.")
    return redirect("aulas:detalhe_professor", pk=aula.pk)


# ---------------------------------------------------------------------------
# Aluno
# ---------------------------------------------------------------------------


def _aluno_do_usuario(usuario):
    return Aluno.objects.select_related("turma").filter(usuario=usuario).first()


@papel_requerido("aluno")
def inicio(request):
    """Página inicial do aluno: as aulas publicadas da sua turma."""
    aluno = _aluno_do_usuario(request.user)
    aulas = []
    if aluno:
        respondidas = set(
            Resposta.objects.filter(aluno=aluno).values_list("questao__aula_id", flat=True).distinct()
        )
        for aula in aluno.turma.aulas.filter(publicada=True):
            aula.respondida = aula.pk in respondidas
            aulas.append(aula)
    return render(request, "aulas/inicio_aluno.html", {"aluno": aluno, "aulas": aulas})


@papel_requerido("aluno")
def ver_aula(request, pk):
    aluno = _aluno_do_usuario(request.user)
    if not aluno:
        raise Http404
    aula = get_object_or_404(Aula, pk=pk, turma=aluno.turma, publicada=True)
    conteudo, questoes = versao_para_aluno(aula, aluno)
    respostas = {r.questao_id: r for r in Resposta.objects.filter(aluno=aluno, questao__aula=aula)}
    chave_tempo = f"aula_{aula.pk}_aberta_em"  # guardada na sessão para medir o tempo até o envio

    if request.method == "POST" and not respostas:
        escolhas = {}
        for questao, _ in questoes:
            try:
                indice = int(request.POST.get(f"questao_{questao.pk}", ""))
            except ValueError:
                indice = None
            if indice is None or not 0 <= indice < len(questao.alternativas):
                messages.error(request, "Responda todas as questões antes de enviar.")
                return redirect("aulas:ver", pk=aula.pk)
            escolhas[questao] = indice

        aberta_em = request.session.pop(chave_tempo, None)
        tempo_ms = int(time.time() * 1000) - aberta_em if aberta_em else None
        try:
            with transaction.atomic():
                for questao, indice in escolhas.items():
                    Resposta.objects.create(
                        aluno=aluno,
                        questao=questao,
                        indice_escolhido=indice,
                        correta=indice == questao.indice_correto,  # gabarito do professor
                        tempo_ms=tempo_ms,
                    )
        except IntegrityError:
            pass  # envio duplicado (ex.: dois cliques); as respostas já estão salvas
        else:
            messages.success(request, "Respostas enviadas!")
        return redirect("aulas:ver", pk=aula.pk)

    if request.method == "POST":
        return redirect("aulas:ver", pk=aula.pk)

    if not respostas and chave_tempo not in request.session:
        request.session[chave_tempo] = int(time.time() * 1000)

    itens = [{"questao": q, "enunciado": enunciado, "resposta": respostas.get(q.pk)} for q, enunciado in questoes]
    contexto = {
        "aula": aula,
        "conteudo": conteudo,
        "itens": itens,
        "respondida": bool(respostas),
        "acertos": sum(1 for r in respostas.values() if r.correta),
    }
    return render(request, "aulas/ver_aula.html", contexto)
