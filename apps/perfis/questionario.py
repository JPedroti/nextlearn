"""Questionário da família — perguntas sobre o dia a dia do aluno que viram sugestões de apoio para o professor.

A família responde com base no que observa em casa. Não há laudo nem diagnóstico: as perguntas
descrevem situações cotidianas, e quem decide quais apoios ativar é o professor.
"""

from .models import APOIOS, Perfil, SugestaoPerfil

# Cada apoio tem 3 perguntas. As respostas vão de 0 (quase nunca) a 2 (com frequência).
# A soma das 3 respostas de um apoio determina se ele é sugerido ao professor.
PERGUNTAS = [
    # --- Atenção e foco (F) ---
    {
        "id": "foco_tarefas_longas",
        "apoio": "foco",
        "texto": "Quando a tarefa é longa ou tem várias etapas, ele para no meio ou desiste antes de terminar?",
    },
    {
        "id": "foco_distracoes",
        "apoio": "foco",
        "texto": "Barulhos, imagens na tela ou movimento ao redor tiram a atenção dele com facilidade?",
    },
    {
        "id": "foco_organizacao",
        "apoio": "foco",
        "texto": "Ele se perde quando precisa organizar várias informações ao mesmo tempo, como datas, nomes ou instruções?",
    },
    # --- Acessibilidade textual (S) ---
    {
        "id": "textual_textos_longos",
        "apoio": "textual",
        "texto": "Ler um texto comprido deixa ele cansado ou confuso antes de chegar ao final?",
    },
    {
        "id": "textual_sentido_literal",
        "apoio": "textual",
        "texto": "Expressões como \"cair a ficha\", \"quebrar a cabeça\" ou \"viajar na maionese\" confundem ele?",
    },
    {
        "id": "textual_palavras_dificeis",
        "apoio": "textual",
        "texto": "Palavras difíceis ou termos técnicos atrapalham: ele trava e não consegue continuar?",
    },
    # --- Interativo e concreto (C) ---
    {
        "id": "concreto_ideias_abstratas",
        "apoio": "concreto",
        "texto": "Conceitos que não dá para ver ou tocar, como frações, átomos ou regras gerais, são mais difíceis para ele?",
    },
    {
        "id": "concreto_exemplos",
        "apoio": "concreto",
        "texto": "Ele só entende uma explicação quando você mostra um exemplo do dia a dia?",
    },
    {
        "id": "concreto_visualizacao",
        "apoio": "concreto",
        "texto": "Desenhar, montar ou imaginar a cena ajuda ele a entender melhor do que só ouvir ou ler?",
    },
]

OPCOES = [(0, "Quase nunca"), (1, "Às vezes"), (2, "Com frequência")]
NOME_OPCAO = dict(OPCOES)

# Soma das 3 respostas de um apoio a partir da qual ele é sugerido ao professor.
# Com 3 perguntas por apoio (0–2 cada), a soma máxima é 6.
# Sugerir com soma >= 3: "com frequência" em 1 pergunta + "às vezes" em outra,
# ou "às vezes" nas 3, ou "com frequência" em 2.
LIMIAR = 3


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
            f"\"{p['texto']}\" {NOME_OPCAO[respostas[p['id']]].lower()}"
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