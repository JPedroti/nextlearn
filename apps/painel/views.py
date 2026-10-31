from django.db.models import Count
from django.shortcuts import render

from apps.contas.decorators import papel_requerido


@papel_requerido("professor")
def inicio(request):
    """Página inicial do professor: as suas turmas."""
    turmas = request.user.turmas.annotate(
        num_alunos=Count("alunos", distinct=True),
        num_aulas=Count("aulas", distinct=True),
    )
    return render(request, "painel/inicio_professor.html", {"turmas": turmas})
