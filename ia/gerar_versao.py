"""Gera (ou reaproveita do cache) a versão adaptada de uma aula para uma máscara de apoios."""

import logging
from datetime import datetime

from apps.aulas.models import VersaoAdaptada
from apps.perfis.models import Perfil, bits_da_mascara

from . import cliente
from .prompt_builder import montar_mensagem, montar_system_prompt

logger = logging.getLogger(__name__)


class ErroGeracao(Exception):
    """Falha que pode ser mostrada ao professor, com a opção de tentar de novo."""


def _info_da_turma(aula, mascara):
    """Busca contexto_familia e historico_ia entre os alunos da turma com a máscara dada.

    Retorna (contexto_familia, historico_ia). Usa o primeiro perfil encontrado.
    """
    from apps.turmas.models import Aluno

    foco, textual, concreto = bits_da_mascara(mascara)
    perfil = (
        Perfil.objects.filter(
            aluno__turma=aula.turma,
            aluno__in=Aluno.objects.filter(turma=aula.turma),
            foco=foco,
            textual=textual,
            concreto=concreto,
            revisado_pelo_professor=True,
        )
        .first()
    )
    if perfil:
        return (
            perfil.contexto_familia if perfil.contexto_familia.strip() else None,
            perfil.historico_ia if perfil.historico_ia.strip() else None,
        )
    return None, None


def gerar_versao(aula, mascara, forcar=False):
    """Devolve a VersaoAdaptada da aula para a máscara (1–7).

    Se ela já existe, devolve a do banco sem chamar a IA (cache). Com `forcar=True`, gera de novo.
    A versão nova sempre fica com aprovada=False: o professor revisa antes de o aluno ver.

    Quando há contexto familiar ou histórico de interações para algum aluno com essa máscara,
    eles são incluídos no system prompt para personalizar a adaptação.
    """
    if not 1 <= mascara <= 7:
        raise ValueError("A máscara precisa estar entre 1 e 7 (0 é a aula original, sem IA).")

    contexto, historico = _info_da_turma(aula, mascara)

    # Sem contexto/histórico, usa o cache normalmente.
    # Com contexto ou histórico, gera sempre (para não misturar versões).
    if not contexto and not historico and not forcar:
        existente = VersaoAdaptada.objects.filter(aula=aula, mascara=mascara).first()
        if existente:
            return existente

    numero_questoes = aula.questoes.count()
    foco, textual, concreto = bits_da_mascara(mascara)
    try:
        saida = cliente.gerar(
            montar_system_prompt(foco, textual, concreto, contexto_familia=contexto, historico_ia=historico),
            montar_mensagem(aula),
        )
    except Exception as erro:
        logger.exception("Erro ao gerar versão da aula %s, máscara %s", aula.pk, mascara)
        raise ErroGeracao("Não foi possível falar com a IA agora. Tente de novo em alguns segundos.") from erro

    if not saida.conteudo.strip() or len(saida.enunciados) != numero_questoes:
        logger.warning(
            "Versão incompleta (aula %s, máscara %s): %s enunciados para %s questões",
            aula.pk, mascara, len(saida.enunciados), numero_questoes,
        )
        raise ErroGeracao("A IA devolveu uma versão incompleta. Tente de novo.")

    versao, _ = VersaoAdaptada.objects.update_or_create(
        aula=aula,
        mascara=mascara,
        defaults={
            "conteudo": saida.conteudo.strip(),
            "enunciados": [enunciado.strip() for enunciado in saida.enunciados],
            "aprovada": False,
        },
    )

    # Registra no histórico de todos os alunos da turma com essa máscara
    agora = datetime.now().strftime("%d/%m %H:%M")
    from apps.turmas.models import Aluno
    foco, textual, concreto = bits_da_mascara(mascara)
    for perfil in Perfil.objects.filter(
        aluno__turma=aula.turma,
        aluno__in=Aluno.objects.filter(turma=aula.turma),
        foco=foco, textual=textual, concreto=concreto,
    ):
        perfil.acrescentar_ao_historico(
            f"[{agora}] Versão adaptada gerada para a aula \"{aula.titulo}\" "
            f"com os apoios: {', '.join(perfil.nomes_apoios())}."
        )

    return versao