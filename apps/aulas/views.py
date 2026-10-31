import time

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.contas.decorators import papel_requerido
from apps.perfis.analise import criar_sugestoes_por_padrao
from apps.perfis.models import Perfil, nomes_da_mascara
from apps.turmas.models import Aluno, Turma
from ia import cliente
from ia.gerar_versao import ErroGeracao, gerar_versao

from .forms import AulaForm, QuestaoFormSet, VersaoForm
from .models import Aula, Resposta, VersaoAdaptada
from .pdf import ErroPDF, extrair_texto, sugerir_titulo
from .versoes import dividir_em_passos, versao_para_aluno

AVISO_IA_NAO_CONFIGURADA = (
    "A geração com IA não está ligada neste servidor (falta a chave GEMINI_API_KEY). "
    "Os alunos continuam vendo a aula original."
)

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
def nova_aula_via_pdf(request, turma_pk):
    """O professor envia um PDF; o texto vira o rascunho do formulário de "Nova aula", que salva a aula normalmente."""
    turma = get_object_or_404(Turma, pk=turma_pk, professor=request.user)
    if request.method == "POST":
        arquivo = request.FILES.get("pdf")
        if not arquivo:
            messages.error(request, "Escolha um arquivo PDF.")
        else:
            try:
                texto = extrair_texto(arquivo)
            except ErroPDF as erro:
                messages.error(request, str(erro))
            else:
                form = AulaForm(initial={"titulo": sugerir_titulo(texto), "conteudo": texto})
                formset = QuestaoFormSet(instance=Aula(turma=turma))
                messages.success(
                    request, "Texto do PDF copiado para a aula. Revise o texto, escreva as questões e salve."
                )
                contexto = {"turma": turma, "form": form, "formset": formset, "acao": reverse("aulas:nova", args=[turma.pk])}
                return render(request, "aulas/form_aula.html", contexto)
    return render(request, "aulas/upload_pdf.html", {"turma": turma})


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
        # O texto original mudou: as versões adaptadas antigas não valem mais.
        apagadas, _ = aula.versoes.all().delete()
        aviso = " As versões adaptadas foram apagadas; gere de novo." if apagadas else ""
        messages.success(request, "Aula atualizada." + aviso)
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    return render(request, "aulas/form_aula.html", {"turma": aula.turma, "form": form, "formset": formset, "aula": aula})


@papel_requerido("professor")
def detalhe_professor(request, pk):
    aula = get_object_or_404(Aula.objects.select_related("turma"), pk=pk, turma__professor=request.user)
    alunos_que_responderam = Aluno.objects.filter(respostas__questao__aula=aula).distinct().count()

    # Uma linha por combinação de apoios que existe na turma (a 000 é a própria aula original).
    alunos_por_mascara = {}
    for perfil in Perfil.objects.filter(aluno__turma=aula.turma):
        if perfil.mascara:
            alunos_por_mascara[perfil.mascara] = alunos_por_mascara.get(perfil.mascara, 0) + 1
    versoes = {versao.mascara: versao for versao in aula.versoes.all()}
    linhas_versoes = [
        {
            "mascara": mascara,
            "apoios": nomes_da_mascara(mascara),
            "num_alunos": num_alunos,
            "versao": versoes.get(mascara),
        }
        for mascara, num_alunos in sorted(alunos_por_mascara.items())
    ]

    contexto = {
        "aula": aula,
        "questoes": aula.questoes.all(),
        "alunos_que_responderam": alunos_que_responderam,
        "total_alunos": aula.turma.alunos.count(),
        "linhas_versoes": linhas_versoes,
        "faltam_aprovar": any(not (linha["versao"] and linha["versao"].aprovada) for linha in linhas_versoes),
        "ia_configurada": cliente.configurado(),
    }
    return render(request, "aulas/detalhe_professor.html", contexto)


@require_POST
@papel_requerido("professor")
def gerar(request, pk, mascara):
    """Gera com a IA a versão da aula para uma combinação de apoios (ou gera de novo, com forcar=1)."""
    aula = get_object_or_404(Aula, pk=pk, turma__professor=request.user)
    if not 1 <= mascara <= 7:
        raise Http404
    if not cliente.configurado():
        messages.error(request, AVISO_IA_NAO_CONFIGURADA)
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    try:
        gerar_versao(aula, mascara, forcar=request.POST.get("forcar") == "1")
    except ErroGeracao as erro:
        messages.error(request, str(erro))
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    return redirect("aulas:revisar_versao", pk=aula.pk, mascara=mascara)


@papel_requerido("professor")
def revisar_versao(request, pk, mascara):
    """Mostra a versão gerada para o professor corrigir, se quiser, e aprovar."""
    aula = get_object_or_404(Aula, pk=pk, turma__professor=request.user)
    versao = get_object_or_404(VersaoAdaptada, aula=aula, mascara=mascara)
    questoes = list(aula.questoes.all())
    form = VersaoForm(request.POST or None, versao=versao, questoes=questoes)
    if request.method == "POST" and form.is_valid():
        versao.conteudo = form.cleaned_data["conteudo"].strip()
        versao.enunciados = form.enunciados()
        versao.aprovada = True
        versao.save()
        messages.success(request, "Versão aprovada: os alunos com esses apoios já veem esta versão.")
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    contexto = {
        "aula": aula,
        "versao": versao,
        "apoios": nomes_da_mascara(mascara),
        "form": form,
        "ia_configurada": cliente.configurado(),
    }
    return render(request, "aulas/revisar_versao.html", contexto)


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
    conteudo, questoes, mascara_vista = versao_para_aluno(aula, aluno)
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
                        versao_mascara=mascara_vista,
                    )
        except IntegrityError:
            pass  # envio duplicado (ex.: dois cliques); as respostas já estão salvas
        else:
            criar_sugestoes_por_padrao(aluno)  # muitos erros → sugestão de apoio para o professor revisar
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
        # Apoio de foco (bit 4): o texto aparece um passo por vez. Nas outras versões, inteiro.
        "passos": dividir_em_passos(conteudo) if mascara_vista & 4 else [],
        "itens": itens,
        "respondida": bool(respostas),
        "acertos": sum(1 for r in respostas.values() if r.correta),
    }
    return render(request, "aulas/ver_aula.html", contexto)
