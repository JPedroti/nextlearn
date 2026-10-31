from django.shortcuts import render

from apps.contas.decorators import papel_requerido


@papel_requerido("familia")
def inicio(request):
    """Página inicial da família."""
    return render(request, "perfis/inicio_familia.html")
