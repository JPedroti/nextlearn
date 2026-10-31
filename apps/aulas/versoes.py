"""Escolhe qual versão da aula cada aluno vê."""

from apps.perfis.models import Perfil

from .models import VersaoAdaptada


def mascara_do_aluno(aluno):
    perfil = Perfil.objects.filter(aluno=aluno).first()
    return perfil.mascara if perfil else 0


def versao_para_aluno(aula, aluno):
    """Devolve o texto da aula e a lista de (questão, enunciado) que este aluno deve ver.

    Máscara 000 (sem apoios): a aula original do professor.
    Outras máscaras: a VersaoAdaptada aprovada pelo professor; se ainda não houver, a original.
    As alternativas e o gabarito continuam vindo sempre de `Questao`.
    """
    questoes = list(aula.questoes.all())
    mascara = mascara_do_aluno(aluno)
    if mascara:
        versao = VersaoAdaptada.objects.filter(aula=aula, mascara=mascara, aprovada=True).first()
        if versao and len(versao.enunciados) == len(questoes):
            return versao.conteudo, list(zip(questoes, versao.enunciados))
    return aula.conteudo, [(questao, questao.enunciado) for questao in questoes]
