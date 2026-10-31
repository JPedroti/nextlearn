from django.shortcuts import render

from apps.contas.decorators import papel_requerido


@papel_requerido("professor")
def inicio(request):
    """Página inicial do professor."""
    return render(request, "painel/inicio_professor.html")
