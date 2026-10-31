from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from apps.contas.decorators import papel_requerido
from apps.turmas.models import Aluno

from .forms import ApoiosForm
from .models import Perfil


@papel_requerido("familia")
def inicio(request):
    """Página inicial da família."""
    return render(request, "perfis/inicio_familia.html")


@papel_requerido("professor")
def editar_apoios(request, aluno_pk):
    """O professor revisa e ajusta os apoios do aluno. A palavra final é dele."""
    aluno = get_object_or_404(Aluno.objects.select_related("usuario", "turma"), pk=aluno_pk, turma__professor=request.user)
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
    form = ApoiosForm(request.POST or None, instance=perfil)
    if request.method == "POST" and form.is_valid():
        perfil = form.save(commit=False)
        perfil.revisado_pelo_professor = True
        perfil.save()
        messages.success(request, f"Apoios de {aluno} salvos.")
        return redirect("turmas:detalhe", pk=aluno.turma.pk)
    return render(request, "perfis/editar_apoios.html", {"aluno": aluno, "form": form})
