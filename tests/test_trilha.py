from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula, Questao, Resposta
from apps.contas.models import Usuario
from apps.perfis.models import Perfil
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"


class TrilhaDoAlunoTests(TestCase):
    """A trilha estilo jogo (mundos com fases em bolinhas e cenário) aparece na página inicial do aluno."""

    def setUp(self):
        professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        turma = Turma.objects.create(nome="7º ano A", professor=professor)
        self.usuario = Usuario.objects.create_user("aluno", password=SENHA, papel=Usuario.Papel.ALUNO)
        self.aluno = Aluno.objects.create(usuario=self.usuario, turma=turma)
        Perfil.objects.create(aluno=self.aluno, foco=True)
        aula = Aula.objects.create(turma=turma, titulo="Frações", conteudo="Uma fração é parte de um todo.", publicada=True)
        self.questao = Questao.objects.create(aula=aula, ordem=1, enunciado="1/2 + 1/2?", alternativas=["1", "2"], indice_correto=0)
        self.client.force_login(self.usuario)

    def test_trilha_aparece_com_fase_atual(self):
        resposta = self.client.get(reverse("prototipo:painel_aluno"))
        self.assertContains(resposta, 'class="trilha"')
        self.assertContains(resposta, "no-atual")

    def test_com_tudo_feito_a_trilha_continua_aberta(self):
        # Com o apoio de foco, só o mundo atual abre. Sem fase atual, o primeiro mundo abre para a trilha não sumir.
        Resposta.objects.create(aluno=self.aluno, questao=self.questao, indice_escolhido=0, correta=True)
        resposta = self.client.get(reverse("prototipo:painel_aluno"))
        self.assertTrue(any(m["aberta"] for m in resposta.context["trilha"]))
