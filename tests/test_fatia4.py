from django.test import TestCase
from django.urls import reverse

from apps.contas.models import Usuario
from apps.perfis.models import Perfil, RespostaQuestionario, SugestaoPerfil
from apps.perfis.questionario import PERGUNTAS, apoios_sugeridos
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"


def respostas(foco=(0, 0, 0), textual=(0, 0, 0), concreto=(0, 0, 0)):
    """Monta {id da pergunta: valor} na ordem das perguntas de cada apoio (3 por apoio)."""
    valores = {"foco": list(foco), "textual": list(textual), "concreto": list(concreto)}
    return {p["id"]: valores[p["apoio"]].pop(0) for p in PERGUNTAS}


class ApoiosSugeridosTests(TestCase):
    def test_todas_quase_nunca_nao_sugere_nada(self):
        self.assertEqual(apoios_sugeridos(respostas()), {"foco": False, "textual": False, "concreto": False})

    def test_um_com_frequencia_basta(self):
        # Com 3 perguntas por apoio, um "com frequência" (2) + dois "quase nunca" (0,0) soma 2 — ainda < 3.
        # Precisa de pelo menos 3: (2,1,0) ou (1,1,1) ou (2,2,0) etc.
        self.assertTrue(apoios_sugeridos(respostas(foco=(2, 1, 0)))["foco"])

    def test_tres_as_vezes_sugerem_e_dois_nao(self):
        # 1+1+1 = 3 → sugere. 1+1+0 = 2 → não sugere.
        self.assertTrue(apoios_sugeridos(respostas(textual=(1, 1, 1)))["textual"])
        self.assertFalse(apoios_sugeridos(respostas(concreto=(1, 1, 0)))["concreto"])


class Fatia4Base(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        usuario = Usuario.objects.create_user("ana", password=SENHA, papel=Usuario.Papel.ALUNO, first_name="Ana")
        self.aluno = Aluno.objects.create(usuario=usuario, turma=self.turma)
        self.perfil = Perfil.objects.create(aluno=self.aluno)

    def criar_familia(self, username="mae_ana", aluno=None):
        familia = Usuario.objects.create_user(username, password=SENHA, papel=Usuario.Papel.FAMILIA)
        aluno = aluno or self.aluno
        aluno.responsavel = familia
        aluno.save()
        return familia

    def dados_questionario(self, **apoios):
        return {chave: str(valor) for chave, valor in respostas(**apoios).items()}


class CadastroFamiliaTests(Fatia4Base):
    def test_professor_cadastra_familia_do_aluno(self):
        self.client.login(username="prof", password=SENHA)
        self.client.post(
            reverse("turmas:nova_familia", args=[self.turma.pk, self.aluno.pk]),
            {"first_name": "Maria", "username": "maria", "password1": SENHA, "password2": SENHA},
        )
        self.aluno.refresh_from_db()
        self.assertEqual(self.aluno.responsavel.username, "maria")
        self.assertEqual(self.aluno.responsavel.papel, Usuario.Papel.FAMILIA)

        self.client.login(username="maria", password=SENHA)
        self.assertContains(self.client.get(reverse("perfis:inicio")), "Responder o questionário")

    def test_outro_professor_nao_cadastra(self):
        Usuario.objects.create_user("outro", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.client.login(username="outro", password=SENHA)
        resposta = self.client.get(reverse("turmas:nova_familia", args=[self.turma.pk, self.aluno.pk]))
        self.assertEqual(resposta.status_code, 404)


class QuestionarioTests(Fatia4Base):
    def setUp(self):
        super().setUp()
        self.familia = self.criar_familia()
        self.client.login(username="mae_ana", password=SENHA)
        self.url = reverse("perfis:questionario", args=[self.aluno.pk])

    def test_respostas_viram_sugestoes_so_onde_mudam_algo(self):
        self.perfil.concreto = True  # o professor já tinha ligado
        self.perfil.save()
        self.client.post(self.url, self.dados_questionario(foco=(2, 1, 0), concreto=(2, 2, 2)))

        questionario = RespostaQuestionario.objects.get(aluno=self.aluno)
        self.assertEqual(questionario.preenchido_por, self.familia)
        sugestoes = SugestaoPerfil.objects.filter(aluno=self.aluno)
        self.assertEqual([(s.campo, s.valor_sugerido) for s in sugestoes], [("foco", True)])
        self.assertIn("Quando a tarefa é longa", sugestoes[0].motivo)
        # As respostas não mudam o perfil sozinhas: o professor decide.
        self.perfil.refresh_from_db()
        self.assertFalse(self.perfil.foco)

    def test_responder_de_novo_substitui_as_sugestoes_pendentes(self):
        self.client.post(self.url, self.dados_questionario(foco=(2, 2, 2)))
        self.client.post(self.url, self.dados_questionario(textual=(2, 2, 2)))
        pendentes = SugestaoPerfil.objects.filter(aluno=self.aluno, status="pendente")
        self.assertEqual([s.campo for s in pendentes], ["textual"])
        self.assertEqual(RespostaQuestionario.objects.filter(aluno=self.aluno).count(), 2)

    def test_questionario_incompleto_nao_salva(self):
        dados = self.dados_questionario()
        dados.pop(PERGUNTAS[0]["id"])
        resposta = self.client.post(self.url, dados)
        self.assertContains(resposta, "Por favor, escolha uma resposta")
        self.assertFalse(RespostaQuestionario.objects.exists())

    def test_familia_nao_responde_por_aluno_de_outra_familia(self):
        usuario = Usuario.objects.create_user("bia", papel=Usuario.Papel.ALUNO)
        outro_aluno = Aluno.objects.create(usuario=usuario, turma=self.turma)
        self.criar_familia("pai_bia", aluno=outro_aluno)
        resposta = self.client.get(reverse("perfis:questionario", args=[outro_aluno.pk]))
        self.assertEqual(resposta.status_code, 404)

    def test_familia_nao_acessa_telas_do_professor(self):
        resposta = self.client.get(reverse("perfis:editar_apoios", args=[self.aluno.pk]))
        self.assertEqual(resposta.status_code, 403)


class RevisaoProfessorTests(Fatia4Base):
    def setUp(self):
        super().setUp()
        self.sugestao = SugestaoPerfil.objects.create(
            aluno=self.aluno, campo="textual", valor_sugerido=True, motivo="teste",
            origem=SugestaoPerfil.Origem.QUESTIONARIO,
        )
        self.client.login(username="prof", password=SENHA)

    def test_aceitar_muda_o_perfil(self):
        self.client.post(reverse("perfis:aceitar_sugestao", args=[self.sugestao.pk]))
        self.perfil.refresh_from_db()
        self.sugestao.refresh_from_db()
        self.assertTrue(self.perfil.textual)
        self.assertTrue(self.perfil.revisado_pelo_professor)
        self.assertEqual(self.sugestao.status, "aceita")

    def test_recusar_mantem_o_perfil(self):
        self.client.post(reverse("perfis:recusar_sugestao", args=[self.sugestao.pk]))
        self.perfil.refresh_from_db()
        self.sugestao.refresh_from_db()
        self.assertFalse(self.perfil.textual)
        self.assertEqual(self.sugestao.status, "recusada")

    def test_volta_para_a_pagina_de_origem_so_se_for_do_proprio_site(self):
        url = reverse("perfis:aceitar_sugestao", args=[self.sugestao.pk])
        resposta = self.client.post(url, {"next": "https://site-malicioso.example/"})
        self.assertRedirects(resposta, reverse("perfis:editar_apoios", args=[self.aluno.pk]), fetch_redirect_response=False)

    def test_outro_professor_nao_responde(self):
        Usuario.objects.create_user("outro", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.client.login(username="outro", password=SENHA)
        resposta = self.client.post(reverse("perfis:aceitar_sugestao", args=[self.sugestao.pk]))
        self.assertEqual(resposta.status_code, 404)
        self.perfil.refresh_from_db()
        self.assertFalse(self.perfil.textual)

    def test_pagina_de_apoios_mostra_sugestoes_e_questionario(self):
        familia = self.criar_familia()
        RespostaQuestionario.objects.create(aluno=self.aluno, respostas=respostas(foco=(2, 0, 0)), preenchido_por=familia)
        resposta = self.client.get(reverse("perfis:editar_apoios", args=[self.aluno.pk]))
        self.assertContains(resposta, "Ligar “Acessibilidade textual”")
        self.assertContains(resposta, "Com frequência")