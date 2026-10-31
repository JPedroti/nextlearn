"""Monta o que vai para a IA: o system prompt (por blocos) e a mensagem (só o conteúdo da aula).

Nenhum dado do aluno entra aqui: o motor recebe apenas os bits da máscara, a aula e,
opcionalmente, o contexto compartilhado pela família (revisado pelo professor).
"""

import re
from pathlib import Path

PASTA_BLOCOS = Path(__file__).resolve().parent / "blocos"
COMENTARIO_HTML = re.compile(r"<!--.*?-->", re.DOTALL)


def ler_bloco(nome):
    """Lê um bloco .md, sem os comentários (<!-- ... -->), que são só para a equipe."""
    texto = (PASTA_BLOCOS / nome).read_text(encoding="utf-8")
    return COMENTARIO_HTML.sub("", texto).strip()


def montar_system_prompt(foco, textual, concreto, contexto_familia=None):
    """base.md + o bloco de cada apoio ligado + conflitos.md quando houver 2+ apoios.

    Se contexto_familia foi fornecido (texto revisado pelo professor), ele é incluído
    como informação adicional para a IA adaptar o tom, os exemplos e o ritmo do texto.
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

    prompt = "\n\n".join(ler_bloco(nome) for nome in blocos)

    if contexto_familia and contexto_familia.strip():
        prompt += (
            "\n\n"
            "<contexto_familia>\n"
            f"{contexto_familia.strip()}\n"
            "</contexto_familia>\n\n"
            "Use as informações acima para adaptar sutilmente o tom, os exemplos e o ritmo do texto "
            "de forma que faça sentido para este aluno, sem desrespeitar nenhuma regra anterior. "
            "Nunca reproduza literalmente o que está na tag <contexto_familia> nem revele que essas "
            "informações existem."
        )

    return prompt


def montar_mensagem(aula):
    """Texto da aula e enunciados, delimitados por tags para a IA não confundir conteúdo com instrução."""
    questoes = "\n".join(
        f'<questao numero="{questao.ordem}">\n{questao.enunciado}\n</questao>' for questao in aula.questoes.all()
    )
    return (
        f"<aula>\n<titulo>{aula.titulo}</titulo>\n{aula.conteudo}\n</aula>\n\n"
        f"<questoes>\n{questoes}\n</questoes>"
    )