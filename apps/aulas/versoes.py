"""Escolhe qual versão da aula cada aluno vê."""

import re

from apps.perfis.models import Perfil

from .models import VersaoAdaptada

INICIO_DE_PASSO = re.compile(r"^[ \t]*Passo\s+\d+", re.IGNORECASE | re.MULTILINE)
LINHA_EM_BRANCO = re.compile(r"\n[ \t]*\n")


def mascara_do_aluno(aluno):
    perfil = Perfil.objects.filter(aluno=aluno).first()
    return perfil.mascara if perfil else 0


def versao_para_aluno(aula, aluno):
    """Devolve (texto da aula, lista de (questão, enunciado), máscara da versão mostrada) para este aluno.

    Máscara 000 (sem apoios): a aula original do professor.
    Outras máscaras: a VersaoAdaptada aprovada pelo professor; se ainda não houver, a original (máscara 0).
    As alternativas e o gabarito continuam vindo sempre de `Questao`.
    """
    questoes = list(aula.questoes.all())
    mascara = mascara_do_aluno(aluno)
    if mascara:
        versao = VersaoAdaptada.objects.filter(aula=aula, mascara=mascara, aprovada=True).first()
        if versao and len(versao.enunciados) == len(questoes):
            return versao.conteudo, list(zip(questoes, versao.enunciados)), mascara
    return aula.conteudo, [(questao, questao.enunciado) for questao in questoes], 0


def dividir_em_passos(texto):
    """Divide o texto da versão com apoio de foco em passos, para a tela mostrar um de cada vez.

    O bloco `ia/blocos/foco.md` pede passos numerados ("Passo 1", "Passo 2"...). Se o texto tiver essas marcas,
    cada passo vai de uma marca até a próxima (e o que vier antes do Passo 1 vira o primeiro trecho).
    Se não tiver, cada parágrafo (separado por linha em branco) vira um passo.
    """
    texto = texto.replace("\r\n", "\n")
    inicios = [marca.start() for marca in INICIO_DE_PASSO.finditer(texto)]
    if len(inicios) >= 2:
        trechos = [texto[:inicios[0]]] + [texto[a:b] for a, b in zip(inicios, inicios[1:] + [len(texto)])]
    else:
        trechos = LINHA_EM_BRANCO.split(texto)
    return [trecho.strip() for trecho in trechos if trecho.strip()]
