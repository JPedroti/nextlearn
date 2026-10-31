"""Relatório da família (números reais do próprio filho) e sugestão de apoio a partir dos acertos."""

from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula, EventoUso, Questao, Resposta
from apps.contas.models import Usuario
from apps.perfis.analise import MINIMO_DE_RESPOSTAS, criar_sugestoes_por_padrao
from apps.perfis.models import Perfil, SugestaoPerfil
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"


class Base(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.familia = Usuario.objects.create_user("mae", password=SENHA, papel=Usuario.Papel.FAMILIA)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        usuario = Usuario.objects.create_user("ana", password=SENHA, papel=Usuario.Papel.ALUNO)
        self.aluno = Aluno.objects.create(usuario=usuario, turma=self.turma, responsavel=self.familia)
        self.perfil = Perfil.objects.create(aluno=self.aluno)
        self.aula = Aula.objects.create(turma=self.turma, titulo="Frações", conteudo="Texto", publicada=True)

    def respostas(self, acertos, erros, versao_mascara=0):
        """Cria questões novas e respostas do aluno: `acertos` certas e `erros` erradas."""
        inicio = self.aula.questoes.count()
        for i in range(acertos + erros):
            questao = Questao.objects.create(
                aula=self.aula, ordem=inicio + i + 1, enunciado=f"Q{i}", alternativas=["a", "b"], indice_correto=0
            )
            certa = i < acertos
            Resposta.objects.create(
                aluno=self.aluno, questao=questao, indice_escolhido=0 if certa else 1, correta=certa,
                versao_mascara=versao_mascara,
            )


class RelatorioFamiliaTests(Base):
    def setUp(self):
        super().setUp()
        self.url = reverse("perfis:relatorio", args=[self.aluno.pk])
        self.client.login(username="mae", password=SENHA)

    def test_sem_respostas(self):
        self.assertContains(self.client.get(self.url), "Nenhuma atividade respondida ainda")

    def test_numeros_reais_e_comparacao_original_adaptada(self):
        self.respostas(acertos=1, erros=1, versao_mascara=0)  # 50% na original
        self.respostas(acertos=3, erros=1, versao_mascara=4)  # 75% na adaptada
        EventoUso.objects.create(aluno=self.aluno, aula=self.aula, tipo="ativou_leitura_voz")
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.context["geral"], {"acertos": 4, "total": 6, "pct": 67})
        self.assertEqual(resposta.context["diferenca"], 25)
        self.assertContains(resposta, "acertou 25 pontos percentuais a mais")
        self.assertContains(resposta, "Leitura em voz alta")

    def test_so_a_familia_do_aluno_ve(self):
        Usuario.objects.create_user("outra", password=SENHA, papel=Usuario.Papel.FAMILIA)
        self.client.login(username="outra", password=SENHA)
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.client.login(username="prof", password=SENHA)
        self.assertEqual(self.client.get(self.url).status_code, 403)


class SugestaoPorAcertosTests(Base):
    def test_poucos_acertos_viram_sugestao_de_linguagem_simples(self):
        self.respostas(acertos=2, erros=MINIMO_DE_RESPOSTAS - 2)
        sugestao = criar_sugestoes_por_padrao(self.aluno)
        self.assertEqual((sugestao.campo, sugestao.valor_sugerido, sugestao.origem), ("textual", True, "padrao_erro"))
        self.assertIn("33%", sugestao.motivo)
        self.perfil.refresh_from_db()
        self.assertFalse(self.perfil.textual)  # o professor decide

    def test_nao_sugere_com_poucas_respostas_nem_com_acertos_suficientes(self):
        self.respostas(acertos=0, erros=MINIMO_DE_RESPOSTAS - 1)
        self.assertIsNone(criar_sugestoes_por_padrao(self.aluno))
        self.respostas(acertos=MINIMO_DE_RESPOSTAS, erros=0)
        self.assertIsNone(criar_sugestoes_por_padrao(self.aluno))

    def test_nao_repete_pendente_nem_recusada_nem_o_que_ja_esta_ligado(self):
        self.respostas(acertos=0, erros=MINIMO_DE_RESPOSTAS)
        criar_sugestoes_por_padrao(self.aluno)
        self.assertIsNone(criar_sugestoes_por_padrao(self.aluno))
        SugestaoPerfil.objects.update(status="recusada")
        self.assertIsNone(criar_sugestoes_por_padrao(self.aluno))
        SugestaoPerfil.objects.all().delete()
        self.perfil.textual = True
        self.perfil.save()
        self.assertIsNone(criar_sugestoes_por_padrao(self.aluno))

    def test_enviar_respostas_na_tela_do_aluno_cria_a_sugestao(self):
        self.respostas(acertos=0, erros=MINIMO_DE_RESPOSTAS - 1)
        outra = Aula.objects.create(turma=self.turma, titulo="Outra", conteudo="Texto", publicada=True)
        questao = Questao.objects.create(aula=outra, ordem=1, enunciado="Q", alternativas=["a", "b"], indice_correto=0)
        self.client.login(username="ana", password=SENHA)
        self.client.post(reverse("aulas:ver", args=[outra.pk]), {f"questao_{questao.pk}": "1"})
        self.assertTrue(SugestaoPerfil.objects.filter(aluno=self.aluno, campo="textual", origem="padrao_erro").exists())
