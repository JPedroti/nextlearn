from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Max
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.aulas.models import Aula, EventoUso, Resposta
from apps.contas.decorators import papel_requerido
from apps.turmas.models import Aluno

from .context_processors import CHAVE_SESSAO
from .forms import ApoiosForm, QuestionarioForm
from .models import PREFERENCIAS, Perfil, RespostaQuestionario, SugestaoPerfil
from .questionario import criar_sugestoes, respostas_legiveis
from .sugestoes import sugerir_pelo_uso

def _redirecionar_para_next(request, padrao, **kwargs):
    """Volta para a página de origem (campo `next`) se ela for deste site; senão, vai para `padrao`."""
    destino = request.POST.get("next", "")
    if url_has_allowed_host_and_scheme(destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()):
        return redirect(destino)
    return redirect(padrao, **kwargs)


# ---------------------------------------------------------------------------
# Aluno
# ---------------------------------------------------------------------------


@require_POST
@papel_requerido("aluno")
def alternar_preferencia(request):
    """Liga ou desliga uma preferência de tela nesta sessão e registra um EventoUso quando o aluno liga."""
    campo = request.POST.get("campo")
    if campo not in PREFERENCIAS:
        return HttpResponseBadRequest("Preferência desconhecida.")
    ligar = request.POST.get("valor") == "1"

    escolhas = request.session.get(CHAVE_SESSAO, {})
    escolhas[campo] = ligar
    request.session[CHAVE_SESSAO] = escolhas

    aluno = Aluno.objects.filter(usuario=request.user).first()
    if ligar and aluno:
        id_aula = request.POST.get("aula", "")
        aula = Aula.objects.filter(pk=id_aula, turma=aluno.turma).first() if id_aula.isdigit() else None
        EventoUso.objects.create(aluno=aluno, aula=aula, tipo=f"ativou_{campo}")
        sugerir_pelo_uso(aluno, campo)

    # A barra usa fetch (JavaScript) para não recarregar a página; sem JavaScript, o formulário volta para a página.
    if request.headers.get("X-Requested-With") == "fetch":
        return JsonResponse({"campo": campo, "valor": ligar})
    return _redirecionar_para_next(request, "aulas:inicio")


# ---------------------------------------------------------------------------
# Família
# ---------------------------------------------------------------------------


@papel_requerido("familia")
def inicio(request):
    """Página inicial da família: os filhos vinculados a esta conta."""
    dependentes = (
        Aluno.objects.filter(responsavel=request.user)
        .select_related("usuario", "turma", "perfil")
        .annotate(ultimo_questionario=Max("questionarios__criado_em"))
    )
    return render(request, "perfis/inicio_familia.html", {"dependentes": dependentes})


@papel_requerido("familia")
def questionario(request, aluno_pk):
    """A família responde as perguntas sobre o dia a dia; as respostas viram sugestões para o professor."""
    aluno = get_object_or_404(Aluno.objects.select_related("usuario"), pk=aluno_pk, responsavel=request.user)
    anterior = aluno.questionarios.first()

    initial = {}
    if anterior:
        initial = anterior.respostas.copy()
        initial["nome_aluno"] = anterior.nome_aluno
        initial["observacoes"] = anterior.observacoes

    form = QuestionarioForm(request.POST or None, initial=initial if anterior else None)
    if request.method == "POST" and form.is_valid():
        dados = form.dados_questionario()
        with transaction.atomic():
            resposta = RespostaQuestionario.objects.create(
                aluno=aluno,
                respostas=dados["respostas"],
                nome_aluno=dados["nome_aluno"],
                observacoes=dados["observacoes"],
                preenchido_por=request.user,
            )
            criar_sugestoes(resposta)
            # Levar as observações para o perfil, para o professor revisar
            if dados["observacoes"].strip():
                perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
                if not perfil.revisado_pelo_professor:
                    perfil.contexto_familia = dados["observacoes"].strip()
                    perfil.save(update_fields=["contexto_familia"])
        messages.success(request, "Obrigado! Suas respostas foram enviadas para o professor, que vai decidir os melhores apoios para o aluno.")
        return redirect("perfis:inicio")
    return render(request, "perfis/questionario.html", {"aluno": aluno, "form": form, "anterior": anterior})


@papel_requerido("familia")
def relatorio(request, aluno_pk):
    """Relatório detalhado de performance do aluno para a família."""
    aluno = get_object_or_404(
        Aluno.objects.select_related("usuario", "turma", "perfil"),
        pk=aluno_pk,
        responsavel=request.user,
    )
    perfil = aluno.perfil if hasattr(aluno, "perfil") else None

    # Respostas do aluno
    respostas = list(
        Resposta.objects.filter(aluno=aluno)
        .select_related("questao__aula")
        .order_by("-criado_em")
    )
    total_respostas = len(respostas)
    acertos = sum(1 for r in respostas if r.correta)

    # Aulas respondidas
    aulas_ids = list(dict.fromkeys(r.questao.aula_id for r in respostas))
    aulas_respondidas = len(aulas_ids)

    # Comparação: original vs adaptada
    originais = [r for r in respostas if r.versao_mascara == 0]
    adaptadas = [r for r in respostas if r.versao_mascara != 0]

    pct_original = round(100 * sum(1 for r in originais if r.correta) / len(originais)) if originais else None
    pct_adaptada = round(100 * sum(1 for r in adaptadas if r.correta) / len(adaptadas)) if adaptadas else None

    # Preferências mais usadas
    from apps.aulas.models import EventoUso
    usos = (
        EventoUso.objects.filter(aluno=aluno)
        .values("tipo")
        .annotate(vezes=Count("id"))
        .order_by("-vezes")
    )
    rotulos_uso = {
        "ativou_fonte_dislexia": "Fonte para dislexia",
        "ativou_leitura_voz": "Leitura em voz alta",
        "ativou_modo_limpo": "Modo limpo",
    }

    contexto = {
        "aluno": aluno,
        "perfil": perfil,
        "total_respostas": total_respostas,
        "acertos": acertos,
        "pct_total": round(100 * acertos / total_respostas) if total_respostas else None,
        "aulas_respondidas": aulas_respondidas,
        "pct_original": pct_original,
        "pct_adaptada": pct_adaptada,
        "num_original": len(originais),
        "num_adaptada": len(adaptadas),
        "usos": [{"rotulo": rotulos_uso.get(u["tipo"], u["tipo"]), "vezes": u["vezes"]} for u in usos],
    }
    return render(request, "perfis/relatorio.html", contexto)


# ---------------------------------------------------------------------------
# Professor
# ---------------------------------------------------------------------------


@papel_requerido("professor")
def editar_apoios(request, aluno_pk):
    """O professor revisa e ajusta os apoios do aluno. A palavra final é dele."""
    aluno = get_object_or_404(
        Aluno.objects.select_related("usuario", "turma", "responsavel"), pk=aluno_pk, turma__professor=request.user
    )
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
    form = ApoiosForm(request.POST or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        perfil = form.save(commit=False)
        perfil.revisado_pelo_professor = True
        perfil.save()
        messages.success(request, f"Apoios de {aluno} salvos.")
        return redirect("turmas:detalhe", pk=aluno.turma.pk)

    ultimo_questionario = aluno.questionarios.select_related("preenchido_por").first()
    contexto = {
        "aluno": aluno,
        "form": form,
        "sugestoes": aluno.sugestoes.filter(status=SugestaoPerfil.Status.PENDENTE),
        "ultimo_questionario": ultimo_questionario,
        "respostas_questionario": respostas_legiveis(ultimo_questionario.respostas) if ultimo_questionario else [],
    }
    return render(request, "perfis/editar_apoios.html", contexto)


@require_POST
@papel_requerido("professor")
def responder_sugestao(request, pk, aceitar):
    """Aceita (aplica no perfil) ou recusa uma sugestão pendente."""
    sugestao = get_object_or_404(
        SugestaoPerfil.objects.select_related("aluno__usuario"),
        pk=pk,
        aluno__turma__professor=request.user,
        status=SugestaoPerfil.Status.PENDENTE,
    )
    if aceitar:
        sugestao.aceitar()
        messages.success(request, f"Sugestão aceita: {sugestao.descricao()} para {sugestao.aluno}.")
    else:
        sugestao.recusar()
        messages.success(request, f"Sugestão recusada para {sugestao.aluno}.")
    return _redirecionar_para_next(request, "perfis:editar_apoios", aluno_pk=sugestao.aluno_id)


@papel_requerido("professor")
def dashboard(request, aluno_pk):
    """Dashboard individual do aluno: métricas de uso, progresso, acertos e apoios."""
    aluno = get_object_or_404(
        Aluno.objects.select_related("usuario", "turma", "perfil"),
        pk=aluno_pk,
        turma__professor=request.user,
    )
    perfil = _perfil(aluno) if hasattr(aluno, "perfil") else None

    respostas = list(
        Resposta.objects.filter(aluno=aluno)
        .select_related("questao__aula")
        .order_by("-criado_em")
    )
    total_questoes = len(respostas)
    acertos = sum(1 for r in respostas if r.correta)

    # Tempo total de uso (ms → minutos)
    tempos = [r.tempo_ms for r in respostas if r.tempo_ms]
    tempo_total_min = round(sum(tempos) / 60000, 1) if tempos else 0

    # Aulas distintas respondidas
    aulas_ids = list(dict.fromkeys(r.questao.aula_id for r in respostas))
    aulas_respondidas = len(aulas_ids)

    # Comparação original vs adaptada
    originais = [r for r in respostas if r.versao_mascara == 0]
    adaptadas = [r for r in respostas if r.versao_mascara != 0]
    pct_original = round(100 * sum(1 for r in originais if r.correta) / len(originais)) if originais else None
    pct_adaptada = round(100 * sum(1 for r in adaptadas if r.correta) / len(adaptadas)) if adaptadas else None

    # Evolução: agrupa respostas por aula
    from collections import defaultdict
    evolucao = []
    for aula_id in aulas_ids:
        suas = [r for r in respostas if r.questao.aula_id == aula_id]
        if suas:
            aula_nome = suas[0].questao.aula.titulo
            data = suas[0].criado_em
            evolucao.append({
                "aula": aula_nome,
                "data": data,
                "acertos": sum(1 for r in suas if r.correta),
                "total": len(suas),
                "pct": round(100 * sum(1 for r in suas if r.correta) / len(suas)),
                "mascara": suas[0].versao_mascara,
            })
    evolucao.sort(key=lambda e: e["data"])

    # Eventos de uso
    from apps.aulas.models import EventoUso
    usos = (
        EventoUso.objects.filter(aluno=aluno)
        .values("tipo")
        .annotate(vezes=Count("id"))
        .order_by("-vezes")
    )
    rotulos_uso = {
        "ativou_fonte_dislexia": "Fonte para dislexia",
        "ativou_leitura_voz": "Leitura em voz alta",
        "ativou_modo_limpo": "Modo limpo",
    }

    # Sugestões pendentes
    sugestoes = aluno.sugestoes.filter(status=SugestaoPerfil.Status.PENDENTE)

    # Último questionário
    ultimo_q = aluno.questionarios.first()

    contexto = {
        "aluno": aluno,
        "perfil": perfil,
        "total_questoes": total_questoes,
        "acertos": acertos,
        "pct_total": round(100 * acertos / total_questoes) if total_questoes else None,
        "tempo_total_min": tempo_total_min,
        "aulas_respondidas": aulas_respondidas,
        "pct_original": pct_original,
        "pct_adaptada": pct_adaptada,
        "num_original": len(originais),
        "num_adaptada": len(adaptadas),
        "evolucao": evolucao,
        "usos": [{"rotulo": rotulos_uso.get(u["tipo"], u["tipo"]), "vezes": u["vezes"]} for u in usos],
        "sugestoes": sugestoes,
        "ultimo_questionario": ultimo_q,
    }
    return render(request, "perfis/dashboard.html", contexto)


def _perfil(aluno):
    try:
        return aluno.perfil
    except Perfil.DoesNotExist:
        return None
