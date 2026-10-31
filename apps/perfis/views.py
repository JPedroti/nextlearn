from django.contrib import messages
from django.db import transaction
from django.db.models import Count, Max
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.aulas.models import Aula, EventoUso, Resposta
from apps.contas.decorators import papel_requerido
from apps.painel.resumo import placar
from apps.turmas.models import Aluno

from .context_processors import CHAVE_SESSAO
from .dicas import dicas_do_perfil
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
        messages.success(request, "Obrigado! Suas respostas foram enviadas para o professor, que vai decidir os melhores apoios para o aluno.")
        return redirect("perfis:inicio")
    return render(request, "perfis/questionario.html", {"aluno": aluno, "form": form, "anterior": anterior})


@papel_requerido("familia")
def relatorio(request, aluno_pk):
    """Números reais do próprio filho para a família: acertos, versão original × adaptada e apoios de leitura usados."""
    aluno = get_object_or_404(Aluno.objects.select_related("usuario", "turma"), pk=aluno_pk, responsavel=request.user)
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
    respostas = list(Resposta.objects.filter(aluno=aluno).select_related("questao"))
    original = placar([r for r in respostas if r.versao_mascara == 0])
    adaptada = placar([r for r in respostas if r.versao_mascara != 0])
    diferenca = adaptada["pct"] - original["pct"] if original["total"] and adaptada["total"] else None
    contexto = {
        "aluno": aluno,
        "perfil": perfil,
        "geral": placar(respostas),
        "aulas_respondidas": len({r.questao.aula_id for r in respostas}),
        "original": original,
        "adaptada": adaptada,
        "diferenca": diferenca,
        "diferenca_absoluta": abs(diferenca) if diferenca is not None else None,
        "usos": _usos_de_leitura(aluno),
        "dicas": dicas_do_perfil(perfil),
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
    """Página de um aluno para o professor: acertos por aula, original × adaptada, apoios de leitura e sugestões."""
    aluno = get_object_or_404(Aluno.objects.select_related("usuario", "turma"), pk=aluno_pk, turma__professor=request.user)
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
    respostas = list(Resposta.objects.filter(aluno=aluno).select_related("questao__aula").order_by("criado_em"))

    por_aula = {}
    for resposta in respostas:
        por_aula.setdefault(resposta.questao.aula, []).append(resposta)
    evolucao = [
        {"aula": aula.titulo, "data": suas[0].criado_em, "mascara": suas[0].versao_mascara, **placar(suas)}
        for aula, suas in por_aula.items()
    ]
    # O tempo é medido por aula (da abertura ao envio) e fica repetido em cada resposta dela: conta uma vez por aula.
    tempos = [suas[0].tempo_ms for suas in por_aula.values() if suas[0].tempo_ms]

    contexto = {
        "aluno": aluno,
        "perfil": perfil,
        "geral": placar(respostas),
        "aulas_respondidas": len(por_aula),
        "tempo_total_min": round(sum(tempos) / 60000, 1) if tempos else 0,
        "original": placar([r for r in respostas if r.versao_mascara == 0]),
        "adaptada": placar([r for r in respostas if r.versao_mascara != 0]),
        "evolucao": evolucao,
        "usos": _usos_de_leitura(aluno),
        "sugestoes": aluno.sugestoes.filter(status=SugestaoPerfil.Status.PENDENTE),
    }
    return render(request, "perfis/dashboard.html", contexto)


def _usos_de_leitura(aluno):
    """[{"rotulo", "vezes"}] de cada apoio de leitura que o aluno ligou, na ordem da barra."""
    vezes = dict(EventoUso.objects.filter(aluno=aluno).values_list("tipo").annotate(vezes=Count("id")))
    return [
        {"rotulo": Perfil._meta.get_field(campo).verbose_name, "vezes": vezes[f"ativou_{campo}"]}
        for campo in PREFERENCIAS
        if vezes.get(f"ativou_{campo}")
    ]
