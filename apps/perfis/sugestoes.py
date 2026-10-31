"""Sugestões de ajuste de perfil a partir do uso: o aluno liga um apoio de leitura várias vezes, e o
sistema pergunta ao professor se ele deve vir ligado desde o início."""

from apps.aulas.models import EventoUso

from .models import Perfil, SugestaoPerfil

# Quantas vezes o aluno precisa ligar o mesmo apoio para virar sugestão.
LIMITE_DE_USOS = 3


def sugerir_pelo_uso(aluno, campo):
    """Cria uma sugestão "ligar <campo>" quando o aluno já ligou esse apoio LIMITE_DE_USOS vezes.

    Não sugere se o apoio já vem ligado no perfil, se já existe uma sugestão pendente igual
    ou se o professor já recusou essa mesma sugestão antes.
    """
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
    if getattr(perfil, campo):
        return None
    vezes = EventoUso.objects.filter(aluno=aluno, tipo=f"ativou_{campo}").count()
    if vezes < LIMITE_DE_USOS:
        return None
    ja_sugerida = SugestaoPerfil.objects.filter(
        aluno=aluno,
        campo=campo,
        valor_sugerido=True,
        origem=SugestaoPerfil.Origem.USO,
        status__in=[SugestaoPerfil.Status.PENDENTE, SugestaoPerfil.Status.RECUSADA],
    ).exists()
    if ja_sugerida:
        return None
    rotulo = Perfil._meta.get_field(campo).verbose_name
    return SugestaoPerfil.objects.create(
        aluno=aluno,
        campo=campo,
        valor_sugerido=True,
        motivo=f"O aluno ligou “{rotulo}” {vezes} vezes. Deixar ligado desde o início?",
        origem=SugestaoPerfil.Origem.USO,
    )
