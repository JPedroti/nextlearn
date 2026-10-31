from django.shortcuts import redirect

from apps.contas.decorators import papel_requerido


@papel_requerido("professor")
def inicio(request):
    """Endereço antigo da área do professor: leva para a área nova (Minha turma)."""
    return redirect("prototipo:professor")
