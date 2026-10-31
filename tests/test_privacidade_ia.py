"""O que vai para a IA: só os apoios (bits) e a aula. Nada do que a família escreve nem dados do aluno."""

from unittest import mock

from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula, Questao, VersaoAdaptada
from apps.contas.models import Usuario
from apps.perfis.models import Perfil, RespostaQuestionario
from apps.perfis.questionario import PERGUNTAS
from apps.turmas.models import Aluno, Turma
from ia.cliente import SaidaVersao
from ia.gerar_versao import gerar_versao

SENHA = "senha-de-teste-123"
OBSERVACAO_SENSIVEL = "Ele tem um diagnóstico e toma remédio de manhã."


class PrivacidadeBase(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.familia = Usuario.objects.create_user("mae", password=SENHA, papel=Usuario.Papel.FAMILIA)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        usuario = Usuario.objects.create_user(
            "juliana", password=SENHA, papel=Usuario.Papel.ALUNO, first_name="Juliana", last_name="Souza"
        )
        self.aluno = Aluno.objects.create(usuario=usuario, turma=self.turma, responsavel=self.familia)
        Perfil.objects.create(aluno=self.aluno, foco=True, revisado_pelo_professor=True)
        self.aula = Aula.objects.create(turma=self.turma, titulo="Frações", conteudo="Uma fração é parte de um todo.")
        Questao.objects.create(aula=self.aula, ordem=1, enunciado="O que é fração?", alternativas=["a", "b"], indice_correto=0)

    def responder_questionario(self):
        self.client.login(username="mae", password=SENHA)
        dados = {p["id"]: "1" for p in PERGUNTAS}
        dados.update(nome_aluno="Juju", observacoes=OBSERVACAO_SENSIVEL)
        self.client.post(reverse("perfis:questionario", args=[self.aluno.pk]), dados)


class OQueVaiParaAIATests(PrivacidadeBase):
    def test_observacoes_da_familia_e_dados_do_aluno_nao_vao_para_a_ia(self):
        self.responder_questionario()
        self.assertEqual(RespostaQuestionario.objects.get().observacoes, OBSERVACAO_SENSIVEL)

        saida = SaidaVersao(conteudo="Passo 1. Texto.", enunciados=["Enunciado"])
        with mock.patch("ia.cliente.gerar", return_value=saida) as gerar:
            gerar_versao(self.aula, 4)
        system_prompt, mensagem = gerar.call_args.args
        for dado in (OBSERVACAO_SENSIVEL, "remédio", "Juju", "Juliana", "Souza", "juliana"):
            self.assertNotIn(dado, system_prompt)
            self.assertNotIn(dado, mensagem)

    def test_cache_vale_mesmo_com_questionario_respondido(self):
        self.responder_questionario()
        saida = SaidaVersao(conteudo="Passo 1. Texto.", enunciados=["Enunciado"])
        with mock.patch("ia.cliente.gerar", return_value=saida) as gerar:
            gerar_versao(self.aula, 4)
            gerar_versao(self.aula, 4)
        self.assertEqual(gerar.call_count, 1)

    def test_gerar_de_novo_sem_forcar_nao_tira_a_aprovacao(self):
        VersaoAdaptada.objects.create(aula=self.aula, mascara=4, conteudo="Aprovada", enunciados=["E"], aprovada=True)
        with mock.patch("ia.cliente.gerar") as gerar:
            versao = gerar_versao(self.aula, 4)
        gerar.assert_not_called()
        self.assertTrue(versao.aprovada)
        self.assertEqual(versao.conteudo, "Aprovada")


class ObservacoesParaOProfessorTests(PrivacidadeBase):
    def test_professor_ve_as_observacoes_com_o_aviso(self):
        self.responder_questionario()
        self.client.login(username="prof", password=SENHA)
        resposta = self.client.get(reverse("perfis:editar_apoios", args=[self.aluno.pk]))
        self.assertContains(resposta, OBSERVACAO_SENSIVEL)
        self.assertContains(resposta, "não vão para a IA")

    def test_questionario_avisa_a_familia(self):
        self.client.login(username="mae", password=SENHA)
        resposta = self.client.get(reverse("perfis:questionario", args=[self.aluno.pk]))
        self.assertContains(resposta, "não é enviado para a inteligência artificial")
