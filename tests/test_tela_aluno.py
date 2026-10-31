"""Tela da aula do aluno: passos do apoio de foco e formulário de respostas que funciona com qualquer número de questões."""

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.aulas.models import Aula, Questao, VersaoAdaptada
from apps.aulas.versoes import dividir_em_passos
from apps.contas.models import Usuario
from apps.perfis.models import Perfil
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"


class DividirEmPassosTests(SimpleTestCase):
    def test_usa_as_marcas_de_passo_e_mantem_os_paragrafos_de_cada_passo(self):
        texto = "Hoje vamos ver frações.\n\nPasso 1: O que é.\n\nUma fração é uma parte.\n\nPasso 2: Como ler.\n\n3/4 é três quartos."
        self.assertEqual(
            dividir_em_passos(texto),
            ["Hoje vamos ver frações.", "Passo 1: O que é.\n\nUma fração é uma parte.", "Passo 2: Como ler.\n\n3/4 é três quartos."],
        )

    def test_sem_marcas_cada_paragrafo_vira_um_passo(self):
        self.assertEqual(dividir_em_passos("Primeiro.\n\nSegundo.\r\n\r\nTerceiro."), ["Primeiro.", "Segundo.", "Terceiro."])

    def test_texto_de_um_paragrafo_so(self):
        self.assertEqual(dividir_em_passos("Só isto."), ["Só isto."])


class TelaDoAlunoTests(TestCase):
    def setUp(self):
        professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=professor)
        self.aula = Aula.objects.create(
            turma=self.turma, titulo="Frações", conteudo="Texto original.\n\nSegundo parágrafo.", publicada=True
        )
        self.questao = Questao.objects.create(aula=self.aula, ordem=1, enunciado="Q1", alternativas=["a", "b"], indice_correto=0)
        VersaoAdaptada.objects.create(
            aula=self.aula, mascara=4, conteudo="Passo 1: Uma ideia.\n\nPasso 2: Outra ideia.", enunciados=["Q1 curta"], aprovada=True
        )
        self.url = reverse("aulas:ver", args=[self.aula.pk])

    def entrar_como_aluno(self, **apoios):
        usuario = Usuario.objects.create_user("ana", password=SENHA, papel=Usuario.Papel.ALUNO)
        Perfil.objects.create(aluno=Aluno.objects.create(usuario=usuario, turma=self.turma), **apoios)
        self.client.login(username="ana", password=SENHA)

    def test_apoio_de_foco_mostra_o_texto_em_passos(self):
        self.entrar_como_aluno(foco=True)
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.context["passos"], ["Passo 1: Uma ideia.", "Passo 2: Outra ideia."])
        self.assertContains(resposta, "data-pagina>", count=2 + 1)  # 2 passos + 1 questão
        self.assertContains(resposta, "Ir para as questões")

    def test_sem_foco_o_texto_aparece_inteiro(self):
        self.entrar_como_aluno()
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.context["passos"], [])
        self.assertNotContains(resposta, 'data-paginas="Passo"')
        self.assertContains(resposta, "Segundo parágrafo.")

    def test_aula_com_uma_questao_pode_ser_enviada(self):
        self.entrar_como_aluno()
        resposta = self.client.get(self.url)
        self.assertContains(resposta, '<button type="submit" class="btn text-lg px-10 py-3">Enviar respostas</button>', html=True)
        self.assertContains(resposta, "required")
        self.client.post(self.url, {f"questao_{self.questao.pk}": "0"})
        self.assertContains(self.client.get(self.url), "1 de 1 acertos")
