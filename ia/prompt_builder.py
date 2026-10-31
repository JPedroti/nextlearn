"""Monta o que vai para a IA: o system prompt (por blocos) e a mensagem (só o conteúdo da aula).

Nenhum dado do aluno entra aqui: o motor recebe apenas os bits da máscara e a aula.
"""

import re
from pathlib import Path

PASTA_BLOCOS = Path(__file__).resolve().parent / "blocos"
COMENTARIO_HTML = re.compile(r"<!--.*?-->", re.DOTALL)


def ler_bloco(nome):
    """Lê um bloco .md, sem os comentários (<!-- ... -->), que são só para a equipe."""
    texto = (PASTA_BLOCOS / nome).read_text(encoding="utf-8")
    return COMENTARIO_HTML.sub("", texto).strip()


def montar_system_prompt(foco, textual, concreto):
    """base.md + o bloco de cada apoio ligado + conflitos.md quando houver 2 ou mais apoios.

    Só os apoios entram aqui: nada do uso das turmas (respostas, acertos, avaliações) vai para a IA.
    As métricas de `ia/metricas.py` ficam fora do prompt (regra de privacidade do CLAUDE.md).
    """
    blocos = ["base.md"]
    if foco:
        blocos.append("foco.md")
    if textual:
        blocos.append("textual.md")
    if concreto:
        blocos.append("concreto.md")
    if sum([bool(foco), bool(textual), bool(concreto)]) >= 2:
        blocos.append("conflitos.md")
    return "\n\n".join(ler_bloco(nome) for nome in blocos)


def montar_mensagem(aula):
    """Texto da aula e enunciados, delimitados por tags para a IA não confundir conteúdo com instrução."""
    questoes = "\n".join(
        f'<questao numero="{questao.ordem}">\n{questao.enunciado}\n</questao>' for questao in aula.questoes.all()
    )
    return (
        f"<aula>\n<titulo>{aula.titulo}</titulo>\n{aula.conteudo}\n</aula>\n\n"
        f"<questoes>\n{questoes}\n</questoes>"
    )
