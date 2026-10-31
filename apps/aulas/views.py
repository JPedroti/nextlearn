import time

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.contas.decorators import papel_requerido
from apps.perfis.models import Perfil, nomes_da_mascara
from apps.turmas.models import Aluno, Turma
from ia.gerar_versao import ErroGeracao, gerar_versao

from .forms import AulaForm, QuestaoFormSet, VersaoForm
from .models import Aula, Resposta, VersaoAdaptada
from .versoes import mascara_do_aluno, versao_para_aluno

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
    }
    return render(request, "aulas/detalhe_professor.html", contexto)


@require_POST
@papel_requerido("professor")
def gerar(request, pk, mascara):
    """Gera com a IA a versão da aula para uma combinação de apoios (ou gera de novo, com forcar=1)."""
    aula = get_object_or_404(Aula, pk=pk, turma__professor=request.user)
    if not 1 <= mascara <= 7:
        raise Http404
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
    contexto = {"aula": aula, "versao": versao, "apoios": nomes_da_mascara(mascara), "form": form}
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
    conteudo, questoes = versao_para_aluno(aula, aluno)
    respostas = {r.questao_id: r for r in Resposta.objects.filter(aluno=aluno, questao__aula=aula)}
    chave_tempo = f"aula_{aula.pk}_aberta_em"  # guardada na sessão para medir o tempo até o envio

    if request.method == "POST" and not respostas:
        escolhas = {}
        for questao, _ in [(q, e) for q, e in questoes if q.tipo == "multipla"]:
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
                        versao_mascara=mascara_do_aluno(aluno),
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
    perfil = Perfil.objects.filter(aluno=aluno).first()
    passos = [p.strip() for p in conteudo.split("\n\n") if p.strip()] if perfil and perfil.foco else []
    contexto = {
        "aula": aula,
        "conteudo": conteudo,
        "passos": passos,
        # Cor das caixas de questão: o apoio mais restritivo do aluno (foco > textual > concreto), skill design-neuro
        "tema_questoes": next((c for c in ("foco", "textual", "concreto") if perfil and getattr(perfil, c)), "base"),
        "itens": itens,
        "itens_multipla": [i for i in itens if i["questao"].tipo == "multipla"],
        "itens_abertos": [i for i in itens if i["questao"].tipo != "multipla"],
        "respondida": bool(respostas),
        "acertos": sum(1 for r in respostas.values() if r.correta),
    }
    return render(request, "aulas/ver_aula.html", contexto)



# ---------------------------------------------------------------------------
# PDF e geração de questões com IA (fluxo do Cauã): PDF/texto → IA sugere → professor revisa → aula rascunho
# ---------------------------------------------------------------------------
@papel_requerido("professor")
def nova_via_pdf(request, turma_pk):
    """Extrai o texto do PDF e abre o formulário normal de nova aula já preenchido (nada é salvo antes)."""
    from .pdf import ErroPDF, extrair_texto, sugerir_titulo

    turma = get_object_or_404(Turma, pk=turma_pk, professor=request.user)
    erro = None
    if request.method == "POST":
        arquivo = request.FILES.get("pdf")
        if not arquivo:
            erro = "Escolha um arquivo PDF."
        else:
            try:
                texto = extrair_texto(arquivo)
            except ErroPDF as e:
                erro = str(e)
            else:
                form = AulaForm(initial={"titulo": sugerir_titulo(texto), "conteudo": texto}, instance=Aula(turma=turma))
                formset = QuestaoFormSet(instance=form.instance)
                return render(request, "aulas/form_aula.html", {"turma": turma, "form": form, "formset": formset,
                                                                "acao": reverse("aulas:nova", args=[turma.pk])})
    return render(request, "aulas/upload_pdf.html", {"turma": turma, "erro": erro}, status=200)


CHAVE_GERACAO = "questoes_geradas"


@papel_requerido("professor")
def gerar_questoes_via_pdf(request, turma_pk):
    from ia import cliente
    from ia.gerar_questoes import ErroGeracaoQuestoes, gerar_questoes

    from .pdf import ErroPDF, extrair_texto, sugerir_titulo

    turma = get_object_or_404(Turma, pk=turma_pk, professor=request.user)
    if not cliente.configurado():
        messages.error(request, "A IA não está configurada neste computador. Crie a aula pelo PDF e escreva as questões.")
        return redirect("aulas:nova_via_pdf", turma_pk=turma.pk)
    if request.method == "POST":
        texto = request.POST.get("texto", "").strip()
        try:
            if request.FILES.get("pdf"):
                texto = extrair_texto(request.FILES["pdf"])
            saida = gerar_questoes(texto, sugerir_titulo(texto))
        except (ErroPDF, ErroGeracaoQuestoes) as e:
            messages.error(request, str(e))
            return render(request, "aulas/gerar_questoes.html", {"turma": turma})
        request.session[CHAVE_GERACAO] = {"turma": turma.pk, "titulo": saida.titulo, "conteudo": texto,
                                          "questoes": [q.model_dump() for q in saida.questoes]}
        return redirect("aulas:revisar_questoes", turma_pk=turma.pk)
    return render(request, "aulas/gerar_questoes.html", {"turma": turma})


def _form_revisao(questoes, dados=None):
    """Formulário dinâmico para revisar as questões sugeridas (tipo, enunciado, alternativas a–d, correta, resposta)."""
    from django import forms

    campos = {}
    for i, q in enumerate(questoes):
        campos[f"{i}_tipo"] = forms.ChoiceField(choices=Questao_TIPOS(), initial=q.get("tipo", "multipla"), label="Tipo")
        campos[f"{i}_enunciado"] = forms.CharField(widget=forms.Textarea(attrs={"rows": 2}), initial=q.get("enunciado", ""), label="Enunciado")
        alts = list(q.get("alternativas") or []) + ["", "", "", ""]
        for k, letra in enumerate("abcd"):
            campos[f"{i}_alt_{letra}"] = forms.CharField(required=False, initial=alts[k], label=letra.upper())
        idx = q.get("indice_correto")
        campos[f"{i}_correta"] = forms.ChoiceField(choices=[(x, x.upper()) for x in "abcd"], widget=forms.RadioSelect, required=False,
                                                   initial="abcd"[idx] if isinstance(idx, int) and 0 <= idx < 4 else "a", label="Correta")
        campos[f"{i}_resposta"] = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}), initial=q.get("resposta_referencia", ""), label="Resposta de referência")
    Classe = type("RevisaoQuestoesForm", (forms.Form,), campos)
    form = Classe(dados) if dados is not None else Classe()
    form.questoes_campos = [{"tipo": form[f"{i}_tipo"], "enunciado": form[f"{i}_enunciado"],
                             "alternativas": [form[f"{i}_alt_{x}"] for x in "abcd"], "correta": form[f"{i}_correta"],
                             "resposta": form[f"{i}_resposta"]} for i in range(len(questoes))]
    return form


def Questao_TIPOS():
    from .models import Questao

    return Questao.TIPOS


@papel_requerido("professor")
def revisar_questoes(request, turma_pk):
    from .models import Questao

    turma = get_object_or_404(Turma, pk=turma_pk, professor=request.user)
    gerado = request.session.get(CHAVE_GERACAO)
    if not gerado or gerado.get("turma") != turma.pk:
        return redirect("aulas:gerar_questoes_via_pdf", turma_pk=turma.pk)
    questoes = gerado["questoes"]
    form = _form_revisao(questoes, request.POST if request.method == "POST" else None)
    titulo = request.POST.get("titulo", gerado["titulo"]) if request.method == "POST" else gerado["titulo"]
    conteudo = request.POST.get("conteudo", gerado["conteudo"]) if request.method == "POST" else gerado["conteudo"]
    if request.method == "POST" and form.is_valid() and titulo.strip() and conteudo.strip():
        d = form.cleaned_data
        with transaction.atomic():
            aula = Aula.objects.create(turma=turma, titulo=titulo.strip()[:200], conteudo=conteudo.strip(), publicada=False)
            for i in range(len(questoes)):
                tipo = d[f"{i}_tipo"]
                alts = [d[f"{i}_alt_{x}"].strip() for x in "abcd" if d[f"{i}_alt_{x}"].strip()]
                correta = "abcd".index(d.get(f"{i}_correta") or "a")
                Questao.objects.create(
                    aula=aula, ordem=i + 1, tipo=tipo, enunciado=d[f"{i}_enunciado"].strip(),
                    alternativas=alts if tipo == "multipla" else [],
                    indice_correto=min(correta, len(alts) - 1) if tipo == "multipla" and alts else None,
                    resposta_referencia="" if tipo == "multipla" else d[f"{i}_resposta"].strip(),
                )
        request.session.pop(CHAVE_GERACAO, None)
        messages.success(request, "Aula criada como rascunho com as questões aprovadas.")
        return redirect("aulas:detalhe_professor", pk=aula.pk)
    return render(request, "aulas/revisar_questoes.html", {"turma": turma, "form": form, "titulo": titulo, "conteudo": conteudo})
