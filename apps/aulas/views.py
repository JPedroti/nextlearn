from django.shortcuts import render

from apps.contas.decorators import papel_requerido


@papel_requerido("aluno")
def inicio(request):
    """Página inicial do aluno."""
    return render(request, "aulas/inicio_aluno.html")
