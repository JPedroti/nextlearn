from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse

from .models import Usuario

# Página inicial de cada papel: as áreas da Chamaleon.
INICIO_POR_PAPEL = {
    Usuario.Papel.PROFESSOR: "prototipo:professor",
    Usuario.Papel.FAMILIA: "prototipo:familia",
    Usuario.Papel.ALUNO: "prototipo:painel_aluno",
}


@login_required
def inicio(request):
    """Depois do login, manda cada pessoa para a área do seu papel."""
    return redirect(INICIO_POR_PAPEL[request.user.papel])


class Entrar(LoginView):
    """Login. A tela de entrada é a da Chamaleon (escolha do papel); este endereço só leva até ela.
    O envio do formulário (POST) continua funcionando aqui, para quem usa o endereço antigo."""

    template_name = "contas/entrar.html"

    def get(self, request, *args, **kwargs):
        destino = reverse("prototipo:entrada")
        consulta = request.GET.urlencode()
        return redirect(f"{destino}?{consulta}" if consulta else destino)
