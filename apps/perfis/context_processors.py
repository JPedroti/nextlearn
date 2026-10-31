"""Preferências de tela do aluno, disponíveis em todos os templates como `preferencias` e `barra_preferencias`."""

from .models import PREFERENCIAS, Perfil

# Escolhas que o aluno fez nesta sessão (ligar/desligar na barra). Valem por cima do padrão do perfil
# até ele sair; o padrão do perfil quem define é o professor.
CHAVE_SESSAO = "preferencias"


def preferencias(request):
    usuario = getattr(request, "user", None)
    if not usuario or not usuario.is_authenticated or usuario.papel != "aluno":
        return {}
    perfil = Perfil.objects.filter(aluno__usuario=usuario).first()
    efetivas = {campo: bool(perfil and getattr(perfil, campo)) for campo in PREFERENCIAS}
    efetivas.update(request.session.get(CHAVE_SESSAO, {}))
    barra = [
        {"campo": campo, "rotulo": Perfil._meta.get_field(campo).verbose_name, "ligado": efetivas[campo]}
        for campo in PREFERENCIAS
    ]
    return {"preferencias": efetivas, "barra_preferencias": barra}
