"""Catálogo das principais demandas de aprendizagem de cada aluno.

Fala de BARREIRAS e APOIOS, nunca de diagnóstico (Decreto 12.686/2025: não se exige laudo).
As demandas vêm de: apoios que o professor escolheu, preferências de tela, questionário da família
e acertos por matéria. O mesmo catálogo aparece para o professor (o que fazer em aula) e para a família
(como organizar o estudo em casa). Evidências: docs/REVISAO_ESPECIALISTAS.md e skill design-neuro.
"""

CATALOGO = {
    "Atenção e foco": {
        "barreira": "Manter a atenção e guardar vários passos ao mesmo tempo",
        "sinais": ["perde o fio em tarefas longas", "esquece o passo seguinte", "distrai com estímulos à volta"],
        "escola": ["Divida a tarefa em passos numerados (Passo 1 de 4).", "Uma instrução por vez, por escrito.", "Pausas curtas a cada 10–15 min."],
        "casa": ["Mesa só com o material da tarefa; celular e TV desligados, fora da vista.",
                 "Blocos de 10–15 min com timer visível e pausa de 3–5 min.",
                 "Lista de passos colada na parede, riscando cada passo feito.",
                 "Sempre o mesmo lugar e horário de estudo."],
        "evidencia": "Treino de memória de trabalho e tarefas em passos (Kofler et al., 2020).",
    },
    "Acessibilidade textual": {
        "barreira": "Ler com fluência e entender textos longos ou com duplo sentido",
        "sinais": ["lê devagar ou cansa ao ler", "confunde palavras parecidas", "entende melhor quando ouve"],
        "escola": ["Frases curtas e literais, sem ironia.", "Ofereça o áudio (botão Ouvir).", "Destaque as palavras-chave do enunciado."],
        "casa": ["Leiam juntos em voz alta ou usem o botão Ouvir.",
                 "Luz boa e sem reflexo na tela ou no papel; letra maior e espaçada ajuda.",
                 "Antes de ler, conte do que o texto trata; depois, peça para ele recontar.",
                 "Explique palavras difíceis com exemplos do dia a dia."],
        "evidencia": "Texto em áudio d = 0,35 (Wood et al., 2018); espaçamento entre letras (Zorzi et al., 2012).",
    },
    "Interativo e concreto": {
        "barreira": "Entender ideias abstratas (números, frações, conceitos) sem um exemplo concreto",
        "sinais": ["trava em contas sem apoio visual", "entende com desenho ou objeto", "esquece regras soltas"],
        "escola": ["Comece por um exemplo do dia a dia.", "Use figura ou material concreto antes da regra.", "Mostre um exemplo resolvido passo a passo."],
        "casa": ["Use objetos de casa: frações com pizza, dinheiro, receitas, medidas.",
                 "Deixe papel e lápis à mão para desenhar o problema.",
                 "Ligue o conteúdo a algo de que ele goste (jogo, esporte, culinária).",
                 "Peça para ele ensinar a você com objetos."],
        "evidencia": "Intervenções digitais em matemática 0,55 (Benavides-Varela et al., 2020).",
    },
}

PREFERENCIA = {
    "Letras espaçadas": "Lê melhor com letras e linhas mais espaçadas.",
    "Ouvir": "Prefere ouvir o texto em voz alta.",
    "Modo limpo": "Se sente melhor com a tela sem enfeites (sensibilidade a estímulos).",
}

AMBIENTE_BASE = ["Horário fixo de estudo, combinado junto.",
                 "Lugar calmo, bem iluminado e sempre o mesmo.",
                 "Pergunte o que aprendeu hoje e peça para explicar com as próprias palavras.",
                 "Elogie o esforço e o progresso, não só a nota."]


def demandas_do_aluno(resumo, medias=None, questionario=None):
    """Recebe o _resumo_aluno (+ médias por matéria e último questionário) e devolve as demandas em ordem."""
    itens = []
    for ap in resumo["apoios"]:
        c = CATALOGO.get(ap)
        if c:
            itens.append({"apoio": ap, "origem": "Apoio escolhido pelo professor", **c})
    if medias:
        mat, med = min(medias.items(), key=lambda kv: kv[1])
        if med < 7:
            itens.append({"apoio": "Reforço", "barreira": f"Dificuldade recente em {mat} (média {med} nas últimas aulas)",
                          "origem": "Acertos nas aulas", "sinais": [], "escola": [f"Retome {mat} com exemplo resolvido e treino curto."],
                          "casa": [f"10 minutos de {mat} com algo concreto do dia a dia, sem cobrança de nota."], "evidencia": ""})
    prefs = [PREFERENCIA[p] for p in resumo.get("prefs", []) if p in PREFERENCIA]
    obs = getattr(questionario, "observacoes", "") if questionario else ""
    ambiente = []
    for i in itens:
        for x in i.get("casa", []):
            if x not in ambiente:
                ambiente.append(x)
    return {"itens": itens, "prefs": prefs, "obs_familia": obs, "ambiente": ambiente or AMBIENTE_BASE,
            "principal": itens[0]["barreira"] if itens else "Sem barreira registrada: segue a aula original"}
