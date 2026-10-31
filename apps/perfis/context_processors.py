"""Tela do aluno em todos os templates: `preferencias`, `barra_preferencias`, `tema` e `apoios_ativos`."""

from .models import PREFERENCIAS, Perfil

# Escolhas que o aluno fez nesta sessão (ligar/desligar na barra). Valem por cima do padrão do perfil
# até ele sair; o padrão do perfil quem define é o professor.
CHAVE_SESSAO = "preferencias"

# Tema de cores da tela (skill design-neuro): vale o apoio de conteúdo mais restritivo que o aluno tem.
# O modo limpo, quando ligado, vale por cima de todos (classe modo-limpo, em static/css/temas.css).
APOIOS_POR_PRIORIDADE = ["foco", "textual", "concreto"]


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
    apoios = [campo for campo in APOIOS_POR_PRIORIDADE if perfil and getattr(perfil, campo)]
    return {
        "preferencias": efetivas,
        "barra_preferencias": barra,
        "tema": apoios[0] if apoios else "base",
        "apoios_ativos": apoios,
    }
