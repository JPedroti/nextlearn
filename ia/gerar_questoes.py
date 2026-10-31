"""Gera questões de estudo a partir do texto de uma aula (digitado ou extraído de um PDF).

A IA SUGERE as questões; o professor revisa, corrige e aprova antes de elas virem conteúdo da aula.
O gabarito final é sempre o que o professor aprovou (regra de ouro: a IA nunca define a correção sozinha).
"""

import logging

from pydantic import BaseModel

from . import cliente
from .prompt_builder import ler_bloco

logger = logging.getLogger(__name__)

BLOCO = "gerar_questoes.md"

TIPOS_VALIDOS = {"multipla", "escrever", "flashcard"}


class SaidaQuestao(BaseModel):
    tipo: str
    enunciado: str
    alternativas: list[str] = []
    indice_correto: int | None = None
    resposta_referencia: str = ""


class SaidaQuestoes(BaseModel):
    titulo: str
    questoes: list[SaidaQuestao]


class ErroGeracaoQuestoes(Exception):
    """Falha que pode ser mostrada ao professor, com a opção de tentar de novo."""


def montar_mensagem(texto, titulo_atual=""):
    """Texto da aula delimitado por tags, para a IA não confundir conteúdo com instrução."""
    cabecalho = f"<titulo>{titulo_atual}</titulo>\n" if titulo_atual else ""
    return f"<aula>\n{cabecalho}{texto}\n</aula>"


def validar_questao(questao, indice):
    """Devolve uma mensagem de erro (ou None) se a questão da IA for inválida."""
    if questao.tipo not in TIPOS_VALIDOS:
        return f"tipo desconhecido '{questao.tipo}'"
    if not questao.enunciado.strip():
        return "sem enunciado"
    if questao.tipo == "multipla":
        if len(questao.alternativas) < 2:
            return "múltipla escolha com menos de 2 alternativas"
        if questao.indice_correto is None or not 0 <= questao.indice_correto < len(questao.alternativas):
            return "índice da alternativa correta inválido"
    else:  # escrever ou flashcard
        if not questao.resposta_referencia.strip():
            return "sem resposta de referência"
    return None


def gerar_questoes(texto, titulo_atual=""):
    """Pede à IA uma lista de questões para o texto. Devolve um SaidaQuestoes (sem salvar nada).

    Erros (API fora do ar, formato inesperado, questões inválidas) sobem como ErroGeracaoQuestoes.
    """
    if not texto.strip():
        raise ErroGeracaoQuestoes("O texto está vazio. Cole ou envie o conteúdo da aula antes de gerar questões.")

    system_prompt = ler_bloco(BLOCO)
    mensagem = montar_mensagem(texto, titulo_atual)

    try:
        saida = cliente.gerar(system_prompt, mensagem, classe_saida=SaidaQuestoes)
    except Exception as erro:
        logger.exception("Erro ao gerar questões")
        raise ErroGeracaoQuestoes("Não foi possível falar com a IA agora. Tente de novo em alguns segundos.") from erro

    if not saida.titulo.strip() or not saida.questoes:
        raise ErroGeracaoQuestoes("A IA não devolveu questões completas. Tente de novo.")

    # Confere cada questão e, se alguma estiver quebrada, recusa a leva inteira (em vez de salvar coisa pela metade).
    for i, questao in enumerate(saida.questoes, start=1):
        problema = validar_questao(questao, i)
        if problema:
            logger.warning("Questão %s inválida %s", i, problema)
            raise ErroGeracaoQuestoes(f"A IA devolveu uma questão inválida ({problema}). Tente de novo.")

    return saida