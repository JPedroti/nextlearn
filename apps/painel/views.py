from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render

from apps.contas.decorators import papel_requerido
from apps.turmas.models import Turma

from .resumo import montar_painel


@papel_requerido("professor")
def inicio(request):
    """Página inicial do professor: as suas turmas."""
    turmas = request.user.turmas.annotate(
        num_alunos=Count("alunos", distinct=True),
        num_aulas=Count("aulas", distinct=True),
        sugestoes_pendentes=Count(
            "alunos__sugestoes", filter=Q(alunos__sugestoes__status="pendente"), distinct=True
        ),
    )
    return render(request, "painel/inicio_professor.html", {"turmas": turmas})


@papel_requerido("professor")
def turma(request, pk):
    """Painel da turma: acertos, versões usadas, apoios de leitura ligados e sugestões de ajuste."""
    turma = get_object_or_404(Turma, pk=pk, professor=request.user)
    return render(request, "painel/turma.html", {"turma": turma, **montar_painel(turma)})
