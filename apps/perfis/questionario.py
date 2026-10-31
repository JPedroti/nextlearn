"""Questionário da família: perguntas sobre o dia a dia que viram sugestões de apoio para o professor.

Não há laudo nem diagnóstico: as perguntas descrevem situações, e quem decide os apoios é o professor.
"""

from .models import APOIOS, Perfil, SugestaoPerfil

# PROVISÓRIO: aguardando as 6 perguntas do Cauã. Para trocar, mude só o "texto" (e o "apoio", se precisar).
PERGUNTAS = [
    {
        "id": "foco_tarefas_longas",
        "apoio": "foco",
        "texto": "Perde a concentração quando a tarefa é longa ou tem muitas etapas?",
    },
    {
        "id": "foco_distracoes",
        "apoio": "foco",
        "texto": "Distrai-se com facilidade com barulhos, imagens ou outras coisas ao redor?",
    },
    {
        "id": "textual_textos_longos",
        "apoio": "textual",
        "texto": "Se perde ou se cansa ao ler textos longos?",
    },
    {
        "id": "textual_sentido_literal",
        "apoio": "textual",
        "texto": "Tem dificuldade com frases de duplo sentido, ironia ou expressões como “cair a ficha”?",
    },
    {
        "id": "concreto_ideias_abstratas",
        "apoio": "concreto",
        "texto": "Tem dificuldade com ideias que não dá para ver ou tocar, como frações ou regras gerais?",
    },
    {
        "id": "concreto_exemplos",
        "apoio": "concreto",
        "texto": "Só entende uma explicação depois de ver um exemplo do dia a dia ou de fazer na prática?",
    },
]

OPCOES = [(0, "Quase nunca"), (1, "Às vezes"), (2, "Com frequência")]
NOME_OPCAO = dict(OPCOES)

# Soma das respostas de um apoio a partir da qual ele é sugerido:
# uma resposta "com frequência", ou duas "às vezes".
LIMIAR = 2


def respostas_legiveis(respostas):
    """[(texto da pergunta, resposta por extenso)] na ordem do questionário, para mostrar ao professor."""
    return [
        (pergunta["texto"], NOME_OPCAO[respostas[pergunta["id"]]])
        for pergunta in PERGUNTAS
        if pergunta["id"] in respostas
    ]


def apoios_sugeridos(respostas):
    """{"foco": bool, "textual": bool, "concreto": bool} a partir das respostas (0–2)."""
    sugeridos = {}
    for campo, _, _ in APOIOS:
        soma = sum(respostas.get(p["id"], 0) for p in PERGUNTAS if p["apoio"] == campo)
        sugeridos[campo] = soma >= LIMIAR
    return sugeridos


def criar_sugestoes(resposta_questionario):
    """Cria uma SugestaoPerfil para cada apoio em que o questionário discorda do perfil atual.

    As sugestões pendentes de um questionário anterior são substituídas pelas novas.
    """
    aluno = resposta_questionario.aluno
    respostas = resposta_questionario.respostas
    perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
    SugestaoPerfil.objects.filter(
        aluno=aluno, origem=SugestaoPerfil.Origem.QUESTIONARIO, status=SugestaoPerfil.Status.PENDENTE
    ).delete()

    criadas = []
    for campo, valor in apoios_sugeridos(respostas).items():
        if getattr(perfil, campo) == valor:
            continue
        detalhes = "; ".join(
            f"“{p['texto']}” {NOME_OPCAO[respostas[p['id']]].lower()}"
            for p in PERGUNTAS
            if p["apoio"] == campo and p["id"] in respostas
        )
        criadas.append(
            SugestaoPerfil.objects.create(
                aluno=aluno,
                campo=campo,
                valor_sugerido=valor,
                motivo=f"Respostas da família: {detalhes}.",
                origem=SugestaoPerfil.Origem.QUESTIONARIO,
            )
        )
    return criadas
