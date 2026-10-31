from django.contrib import messages
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from apps.contas.decorators import papel_requerido
from apps.contas.models import Usuario
from apps.perfis.models import Perfil

from .forms import NovoAlunoForm, TurmaForm
from .models import Aluno, Turma


@papel_requerido("professor")
def nova_turma(request):
    form = TurmaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        turma = form.save(commit=False)
        turma.professor = request.user
        turma.save()
        messages.success(request, f"Turma “{turma}” criada.")
        return redirect("turmas:detalhe", pk=turma.pk)
    return render(request, "turmas/nova_turma.html", {"form": form})


@papel_requerido("professor")
def detalhe(request, pk):
    # Filtrar por professor garante que ninguém abre a turma de outro professor.
    turma = get_object_or_404(Turma, pk=pk, professor=request.user)
    contexto = {
        "turma": turma,
        "alunos": turma.alunos.select_related("usuario", "perfil"),
        "aulas": turma.aulas.all(),
    }
    return render(request, "turmas/detalhe.html", contexto)


@papel_requerido("professor")
def novo_aluno(request, pk):
    turma = get_object_or_404(Turma, pk=pk, professor=request.user)
    form = NovoAlunoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            usuario = form.save(commit=False)
            usuario.papel = Usuario.Papel.ALUNO
            usuario.save()
            aluno = Aluno.objects.create(usuario=usuario, turma=turma)
            Perfil.objects.create(aluno=aluno)  # começa sem apoios: vê a aula original
        messages.success(
            request, f"{usuario} foi cadastrado(a). Passe o usuário “{usuario.username}” e a senha para o primeiro acesso."
        )
        return redirect("turmas:detalhe", pk=turma.pk)
    return render(request, "turmas/novo_aluno.html", {"turma": turma, "form": form})
