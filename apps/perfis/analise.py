"""Sugestão de apoio a partir dos acertos do aluno.

Uma regra só, simples de explicar: depois de pelo menos MINIMO_DE_RESPOSTAS questões respondidas, se o aluno
acertou menos da metade e ainda não tem o apoio de acessibilidade textual, o professor recebe a sugestão de ligá-lo
(para ver se a dificuldade está no texto). Como nas outras sugestões, nada muda sozinho: o professor aceita ou recusa.
"""

from apps.aulas.models import Resposta

from .models import Perfil, SugestaoPerfil

MINIMO_DE_RESPOSTAS = 6
LIMITE_DE_ACERTOS = 50  # em %


def criar_sugestoes_por_padrao(aluno):
    """Cria a sugestão "ligar Acessibilidade textual" quando a regra acima vale. Devolve a sugestão ou None.

    Não sugere de novo se já existe uma sugestão pendente igual (de qualquer origem) ou se o professor já recusou
    esta mesma sugestão vinda dos acertos.
    """
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
    if perfil.textual:
        return None
    respostas = Resposta.objects.filter(aluno=aluno)
    total = respostas.count()
    if total < MINIMO_DE_RESPOSTAS:
        return None
    acertos = respostas.filter(correta=True).count()
    pct = round(100 * acertos / total)
    if pct >= LIMITE_DE_ACERTOS:
        return None

    iguais = SugestaoPerfil.objects.filter(aluno=aluno, campo="textual", valor_sugerido=True)
    if iguais.filter(status=SugestaoPerfil.Status.PENDENTE).exists():
        return None
    if iguais.filter(origem=SugestaoPerfil.Origem.PADRAO_ERRO, status=SugestaoPerfil.Status.RECUSADA).exists():
        return None

    return SugestaoPerfil.objects.create(
        aluno=aluno,
        campo="textual",
        valor_sugerido=True,
        motivo=(
            f"O aluno acertou {pct}% das {total} questões que respondeu. Ligar a linguagem simples ajuda a ver "
            "se a dificuldade está no texto."
        ),
        origem=SugestaoPerfil.Origem.PADRAO_ERRO,
    )
