from django.contrib import messages
from django.db import transaction
from django.db.models import Max
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from apps.aulas.models import Aula, EventoUso
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
    form = QuestionarioForm(request.POST or None, initial=anterior.respostas if anterior else None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            resposta = RespostaQuestionario.objects.create(
                aluno=aluno, respostas=form.cleaned_data, preenchido_por=request.user
            )
            criar_sugestoes(resposta)
        messages.success(request, "Obrigado! As respostas foram para o professor, que decide os apoios.")
        return redirect("perfis:inicio")
    return render(request, "perfis/questionario.html", {"aluno": aluno, "form": form, "anterior": anterior})


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
