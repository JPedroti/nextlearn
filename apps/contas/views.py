from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import Usuario

# Página inicial de cada papel.
INICIO_POR_PAPEL = {
    Usuario.Papel.PROFESSOR: "painel:inicio",
    Usuario.Papel.FAMILIA: "perfis:inicio",
    Usuario.Papel.ALUNO: "aulas:inicio",
}


@login_required
def inicio(request):
    """Depois do login, manda cada pessoa para a página do seu papel."""
    return redirect(INICIO_POR_PAPEL[request.user.papel])
