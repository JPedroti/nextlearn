"""Escolhe qual versão da aula cada aluno vê."""


def versao_para_aluno(aula, aluno):
    """Devolve o texto da aula e a lista de (questão, enunciado) que este aluno deve ver.

    Fatia 1: sempre a versão original do professor (máscara 000).
    Fatia 2: usar a VersaoAdaptada aprovada da máscara do aluno, quando existir.
    As alternativas e o gabarito continuam vindo sempre de `Questao`.
    """
    questoes = list(aula.questoes.all())
    return aula.conteudo, [(questao, questao.enunciado) for questao in questoes]
