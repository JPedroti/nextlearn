"""Conteúdo de EXEMPLO para desenhar as telas. Nada aqui é dado de aluno real nem vai para a demo oficial.

As versões adaptadas abaixo foram escritas à mão para mostrar o formato de cada apoio; no app real,
elas vêm de VersaoAdaptada (geradas pela IA e aprovadas pelo professor).
"""

AULA = {
    "titulo": "Frações: partes de um inteiro",
    "turma": "6º ano A",
    "original": [
        "Uma fração representa uma parte de um todo que foi dividido em partes iguais. O número de baixo, chamado denominador, indica em quantas partes iguais o inteiro foi dividido. O número de cima, o numerador, indica quantas dessas partes estamos considerando.",
        "Por exemplo, na fração 3/4, o inteiro foi dividido em 4 partes iguais e estamos considerando 3 delas. Quanto maior o denominador, menores ficam as partes, pois o mesmo inteiro é repartido entre mais pedaços.",
        "Para comparar frações com o mesmo denominador, basta comparar os numeradores: 3/8 é maior que 1/8, pois 3 partes são mais do que 1 parte do mesmo tamanho.",
    ],
}

# Versões por máscara (F*4 + S*2 + C*1). Máscaras sem versão própria usam a mais próxima (ver views.py).
VERSOES = {
    4: {  # Atenção e foco: passos curtos, um de cada vez
        "passos": [
            ("Passo 1", "Uma fração mostra uma parte de um inteiro dividido em partes iguais."),
            ("Passo 2", "O número de baixo é o denominador. Ele diz em quantas partes iguais o inteiro foi dividido."),
            ("Passo 3", "O número de cima é o numerador. Ele diz quantas partes estamos considerando."),
            ("Passo 4", "Em 3/4, o inteiro tem 4 partes iguais. Estamos considerando 3."),
            ("Passo 5", "Mesmo denominador? Compare os numeradores. 3/8 é maior que 1/8."),
        ],
    },
    2: {  # Acessibilidade textual: frases curtas e literais, termos explicados
        "paragrafos": [
            "Uma fração mostra uma parte de uma coisa inteira. A coisa inteira foi dividida em partes do mesmo tamanho.",
            "A fração tem dois números. O número de baixo se chama denominador. O denominador diz em quantas partes a coisa inteira foi dividida. O número de cima se chama numerador. O numerador diz quantas partes estamos contando.",
            "Exemplo: na fração 3/4, a coisa inteira foi dividida em 4 partes. Estamos contando 3 partes.",
            "Quando o denominador é maior, cada parte fica menor. A mesma coisa inteira é dividida em mais partes.",
            "Duas frações com o mesmo denominador: olhe o numerador. O numerador maior mostra a fração maior. Por isso, 3/8 é maior que 1/8.",
        ],
    },
    1: {  # Interativo e concreto: exemplo do dia a dia + representação visual
        "paragrafos": [
            "Imagine uma pizza cortada em 4 fatias iguais. Cada fatia é 1/4 da pizza. Se você come 3 fatias, comeu 3/4 da pizza.",
            "O número de baixo (denominador) é em quantas fatias a pizza foi cortada. O número de cima (numerador) é quantas fatias você pegou.",
            "Se a mesma pizza for cortada em 8 fatias, cada fatia fica menor. Por isso, mais fatias significa fatias menores.",
            "Com o mesmo número de fatias, quem pegou mais fatias comeu mais: 3/8 é mais pizza que 1/8.",
        ],
        "visual": [  # barras de fração desenhadas na tela
            {"rotulo": "3/4", "partes": 4, "marcadas": 3},
            {"rotulo": "3/8", "partes": 8, "marcadas": 3},
            {"rotulo": "1/8", "partes": 8, "marcadas": 1},
        ],
    },
    6: {  # Foco + textual: passos curtos com frases simples
        "passos": [
            ("Passo 1", "Uma fração mostra uma parte de uma coisa inteira."),
            ("Passo 2", "A coisa inteira foi dividida em partes do mesmo tamanho."),
            ("Passo 3", "O número de baixo é o denominador. Ele diz em quantas partes a coisa foi dividida."),
            ("Passo 4", "O número de cima é o numerador. Ele diz quantas partes estamos contando."),
            ("Passo 5", "Mesmo denominador: o numerador maior mostra a fração maior. 3/8 é maior que 1/8."),
        ],
    },
    7: {  # Os três: passos curtos, frases simples, um exemplo concreto por passo
        "passos": [
            ("Passo 1", "Pense numa pizza inteira. Uma fração mostra uma parte dela."),
            ("Passo 2", "A pizza foi cortada em 4 fatias iguais. O número 4 fica embaixo. Ele se chama denominador."),
            ("Passo 3", "Você pegou 3 fatias. O número 3 fica em cima. Ele se chama numerador. Você pegou 3/4 da pizza."),
            ("Passo 4", "Pizza cortada em 8 fatias: 3 fatias (3/8) é mais que 1 fatia (1/8)."),
        ],
        "visual": [{"rotulo": "3/4", "partes": 4, "marcadas": 3}],
    },
}

QUESTOES = [
    {
        "original": "Na fração 5/6, o que indica o número 6?",
        "simples": "Na fração 5/6, o que o número 6 mostra?",
        "alternativas": ["Quantas partes foram consideradas", "Em quantas partes iguais o inteiro foi dividido", "O resultado da divisão"],
        "correta": 1,
    },
    {
        "original": "Qual fração é maior: 2/7 ou 5/7?",
        "simples": "Qual fração é maior: 2/7 ou 5/7?",
        "alternativas": ["2/7", "5/7", "São iguais"],
        "correta": 1,
    },
    {
        "original": "Um bolo foi dividido em 8 partes iguais e foram comidas 3. Que fração do bolo foi comida?",
        "simples": "Um bolo tem 8 pedaços iguais. Foram comidos 3 pedaços. Que fração do bolo foi comida?",
        "alternativas": ["3/8", "8/3", "5/8"],
        "correta": 0,
    },
]

AULAS_ALUNO = [
    {"titulo": "Frações: partes de um inteiro", "materia": "Matemática", "status": "nova"},
    {"titulo": "O ciclo da água", "materia": "Ciências", "status": "nova"},
    {"titulo": "Substantivos próprios e comuns", "materia": "Português", "status": "feita", "acertos": "4 de 5"},
]

# Turma de exemplo para o painel do professor (nomes genéricos de propósito)
ALUNOS = [
    {"nome": "Aluno A", "mascara": 0, "acertos": 80, "prefs": []},
    {"nome": "Aluno B", "mascara": 4, "acertos": 67, "prefs": ["Modo limpo"]},
    {"nome": "Aluno C", "mascara": 2, "acertos": 100, "prefs": ["Leitura em voz alta", "Letras espaçadas"]},
    {"nome": "Aluno D", "mascara": 6, "acertos": 33, "prefs": []},
    {"nome": "Aluno E", "mascara": 1, "acertos": 67, "prefs": []},
    {"nome": "Aluno F", "mascara": 0, "acertos": None, "prefs": []},
]

SUGESTOES = [
    {"aluno": "Aluno D", "acao": "Ligar “Leitura em voz alta”", "motivo": "Ligou a leitura em voz alta em 3 aulas.", "origem": "Uso da plataforma"},
    {"aluno": "Aluno E", "acao": "Ligar “Acessibilidade textual”", "motivo": "Respostas da família: “se cansa ao ler textos longos” com frequência.", "origem": "Questionário da família"},
]

DICAS_FAMILIA = {
    "foco": "Estudar em blocos curtos (10 a 15 min), num lugar sem TV e com o celular longe.",
    "textual": "Ler junto: o adulto lê uma frase, a criança lê a próxima. Perguntar o que entendeu com as próprias palavras.",
    "concreto": "Usar objetos da casa: dividir uma pizza, uma barra de chocolate ou uma folha em partes iguais.",
    "base": "Perguntar o que aprendeu hoje e pedir para explicar com um exemplo.",
}
