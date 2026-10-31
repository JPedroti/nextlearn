"""Extrai o texto de um PDF enviado pelo professor, para virar o rascunho de uma aula nova.

Só o texto vai para o formulário de "Nova aula", onde o professor revisa, escreve as questões e salva.
O arquivo não é guardado e não vai para a IA.
"""

import logging

from pypdf import PdfReader

logger = logging.getLogger(__name__)

TAMANHO_MAXIMO_MB = 10


class ErroPDF(Exception):
    """Problema com o arquivo, explicado em linguagem simples para o professor."""


def extrair_texto(arquivo):
    """Devolve o texto de todas as páginas, separadas por uma linha em branco."""
    if not arquivo.name.lower().endswith(".pdf"):
        raise ErroPDF("Envie um arquivo PDF.")
    if arquivo.size > TAMANHO_MAXIMO_MB * 1024 * 1024:
        raise ErroPDF(f"O arquivo passa de {TAMANHO_MAXIMO_MB} MB. Envie um PDF menor.")
    try:
        paginas = [(pagina.extract_text() or "").strip() for pagina in PdfReader(arquivo).pages]
    except Exception as erro:  # arquivo corrompido, protegido por senha etc.: qualquer falha vira a mesma mensagem
        logger.warning("Não foi possível ler o PDF %s: %s", arquivo.name, erro)
        raise ErroPDF("Não foi possível ler este arquivo como PDF.") from erro
    texto = "\n\n".join(pagina for pagina in paginas if pagina)
    if not texto:
        raise ErroPDF(
            "Este PDF não tem texto que dê para copiar (parece digitalizado). "
            "Use “Nova aula” e cole o texto da aula."
        )
    return texto


def sugerir_titulo(texto, limite=200):
    """A primeira linha com texto vira a sugestão de título (o professor pode mudar)."""
    for linha in texto.splitlines():
        if linha.strip():
            return linha.strip()[:limite]
    return ""
