"""Dicas práticas para a família fazer em casa, uma lista por apoio que o professor ligou (skill design-neuro).

São orientações gerais escritas pela equipe, em linguagem simples e sem diagnóstico; não são parâmetros medidos.
"""

from .models import APOIOS

DICAS_PARA_CASA = {
    "foco": [
        "Divida a lição de casa em partes pequenas e combine uma pausa curta entre elas.",
        "Deixe na mesa só o material da tarefa da vez.",
        "Antes de começar, conte quantos passos a tarefa tem e risque cada um quando terminar.",
    ],
    "textual": [
        "Leiam juntos em voz alta e peça para ele(a) contar, com as próprias palavras, o que entendeu.",
        "Quando aparecer uma palavra difícil, troque por uma do dia a dia e volte ao texto.",
        "Prefira perguntas diretas, com uma ideia por vez.",
    ],
    "concreto": [
        "Use coisas da casa para mostrar a ideia: dividir uma pizza, contar dinheiro, medir uma receita.",
        "Peça um exemplo do dia a dia para cada coisa nova que ele(a) aprendeu.",
        "Desenhar a situação junto ajuda a entender antes de fazer a conta.",
    ],
}


def dicas_do_perfil(perfil):
    """[(nome do apoio, [dicas])] para os apoios de conteúdo ligados no perfil, na ordem dos apoios."""
    return [(nome, DICAS_PARA_CASA[campo]) for campo, nome, _ in APOIOS if getattr(perfil, campo)]
