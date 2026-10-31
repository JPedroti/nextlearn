from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula, Questao, Resposta
from apps.contas.models import Usuario
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"


def dados_aula(questoes, titulo="Frações", conteudo="Uma fração representa partes de um todo."):
    """Monta o POST do formulário de aula com o formset de questões (5 formulários: 1 mínimo + 4 extras)."""
    total = max(5, len(questoes))
    dados = {
        "titulo": titulo,
        "conteudo": conteudo,
        "questoes-TOTAL_FORMS": str(total),
        "questoes-INITIAL_FORMS": "0",
        "questoes-MIN_NUM_FORMS": "1",
        "questoes-MAX_NUM_FORMS": "1000",
    }
    for i, q in enumerate(questoes):
        for chave, valor in q.items():
            dados[f"questoes-{i}-{chave}"] = valor
    return dados


class Fatia1Base(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)

    def criar_aluno(self, username, turma=None):
        usuario = Usuario.objects.create_user(username, password=SENHA, papel=Usuario.Papel.ALUNO)
        return Aluno.objects.create(usuario=usuario, turma=turma or self.turma)

    def criar_aula(self, publicada=True):
        aula = Aula.objects.create(turma=self.turma, titulo="Frações", conteudo="Texto", publicada=publicada)
        Questao.objects.create(aula=aula, ordem=1, enunciado="Quanto é 1/2 de 10?", alternativas=["2", "5", "10"], indice_correto=1)
        Questao.objects.create(aula=aula, ordem=2, enunciado="1/4 é maior que 1/2?", alternativas=["Sim", "Não"], indice_correto=1)
        return aula


class ProfessorTests(Fatia1Base):
    def setUp(self):
        super().setUp()
        self.client.login(username="prof", password=SENHA)

    def test_cria_turma(self):
        resposta = self.client.post(reverse("turmas:nova"), {"nome": "7º B"})
        turma = Turma.objects.get(nome="7º B")
        self.assertEqual(turma.professor, self.professor)
        self.assertRedirects(resposta, reverse("turmas:detalhe", args=[turma.pk]))

    def test_nao_ve_turma_de_outro_professor(self):
        outro = Usuario.objects.create_user("outro", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        turma_alheia = Turma.objects.create(nome="Outra", professor=outro)
        self.assertEqual(self.client.get(reverse("turmas:detalhe", args=[turma_alheia.pk])).status_code, 404)

    def test_cadastra_aluno_na_turma(self):
        self.client.post(
            reverse("turmas:novo_aluno", args=[self.turma.pk]),
            {"first_name": "Ana", "last_name": "Souza", "username": "ana", "password1": SENHA, "password2": SENHA},
        )
        aluno = Aluno.objects.get(usuario__username="ana")
        self.assertEqual(aluno.turma, self.turma)
        self.assertEqual(aluno.usuario.papel, Usuario.Papel.ALUNO)
        self.assertTrue(self.client.login(username="ana", password=SENHA))

    def test_cria_aula_com_questoes_e_gabarito(self):
        dados = dados_aula([
            {"enunciado": "Quanto é 1/2 de 10?", "alternativa_a": "2", "alternativa_b": "5", "alternativa_c": "10", "correta": "B"},
            # Alternativa B vazia: as preenchidas são A e C, e C (a correta) vira o índice 1.
            {"enunciado": "1/4 é maior que 1/2?", "alternativa_a": "Sim", "alternativa_c": "Não", "correta": "C"},
        ])
        self.client.post(reverse("aulas:nova", args=[self.turma.pk]), dados)
        aula = Aula.objects.get(titulo="Frações")
        self.assertFalse(aula.publicada)
        q1, q2 = aula.questoes.all()
        self.assertEqual((q1.ordem, q1.alternativas, q1.indice_correto), (1, ["2", "5", "10"], 1))
        self.assertEqual((q2.ordem, q2.alternativas, q2.indice_correto), (2, ["Sim", "Não"], 1))

    def test_aula_sem_questao_nao_e_criada(self):
        resposta = self.client.post(reverse("aulas:nova", args=[self.turma.pk]), dados_aula([]))
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Aula.objects.exists())

    def test_correta_vazia_e_recusada(self):
        dados = dados_aula([{"enunciado": "?", "alternativa_a": "x", "alternativa_b": "y", "correta": "D"}])
        resposta = self.client.post(reverse("aulas:nova", args=[self.turma.pk]), dados)
        self.assertContains(resposta, "A alternativa marcada como correta está vazia.")
        self.assertFalse(Aula.objects.exists())

    def test_publicar_e_despublicar(self):
        aula = self.criar_aula(publicada=False)
        url = reverse("aulas:alternar_publicacao", args=[aula.pk])
        self.client.post(url)
        aula.refresh_from_db()
        self.assertTrue(aula.publicada)
        self.client.post(url)
        aula.refresh_from_db()
        self.assertFalse(aula.publicada)

    def test_nao_edita_aula_com_respostas(self):
        aula = self.criar_aula()
        aluno = self.criar_aluno("ana")
        questao = aula.questoes.first()
        Resposta.objects.create(aluno=aluno, questao=questao, indice_escolhido=0, correta=False)
        resposta = self.client.get(reverse("aulas:editar", args=[aula.pk]))
        self.assertRedirects(resposta, reverse("aulas:detalhe_professor", args=[aula.pk]))


class AlunoTests(Fatia1Base):
    def setUp(self):
        super().setUp()
        self.aluno = self.criar_aluno("ana")
        self.client.login(username="ana", password=SENHA)

    def test_ve_so_aulas_publicadas_da_sua_turma(self):
        publicada = self.criar_aula(publicada=True)
        rascunho = self.criar_aula(publicada=False)
        self.assertEqual(self.client.get(reverse("aulas:ver", args=[publicada.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("aulas:ver", args=[rascunho.pk])).status_code, 404)

        outra_turma = Turma.objects.create(nome="Outra", professor=self.professor)
        aula_alheia = Aula.objects.create(turma=outra_turma, titulo="X", conteudo="Y", publicada=True)
        self.assertEqual(self.client.get(reverse("aulas:ver", args=[aula_alheia.pk])).status_code, 404)

    def test_ve_a_versao_original_do_professor(self):
        aula = self.criar_aula()
        resposta = self.client.get(reverse("aulas:ver", args=[aula.pk]))
        self.assertContains(resposta, "Quanto é 1/2 de 10?")

    def test_responde_e_correcao_usa_gabarito_do_professor(self):
        aula = self.criar_aula()
        q1, q2 = aula.questoes.all()
        url = reverse("aulas:ver", args=[aula.pk])
        self.client.get(url)
        self.client.post(url, {f"questao_{q1.pk}": "1", f"questao_{q2.pk}": "0"})
        self.assertTrue(Resposta.objects.get(aluno=self.aluno, questao=q1).correta)
        self.assertFalse(Resposta.objects.get(aluno=self.aluno, questao=q2).correta)
        self.assertIsNotNone(Resposta.objects.get(aluno=self.aluno, questao=q1).tempo_ms)
        self.assertContains(self.client.get(url), "1 de 2 acertos")

    def test_nao_responde_duas_vezes(self):
        aula = self.criar_aula()
        q1, q2 = aula.questoes.all()
        url = reverse("aulas:ver", args=[aula.pk])
        self.client.post(url, {f"questao_{q1.pk}": "1", f"questao_{q2.pk}": "1"})
        self.client.post(url, {f"questao_{q1.pk}": "0", f"questao_{q2.pk}": "0"})
        self.assertEqual(Resposta.objects.filter(aluno=self.aluno).count(), 2)
        self.assertTrue(Resposta.objects.get(aluno=self.aluno, questao=q1).correta)

    def test_envio_incompleto_nao_salva(self):
        aula = self.criar_aula()
        q1 = aula.questoes.first()
        self.client.post(reverse("aulas:ver", args=[aula.pk]), {f"questao_{q1.pk}": "1"})
        self.assertFalse(Resposta.objects.exists())

    def test_aluno_nao_acessa_telas_do_professor(self):
        resposta = self.client.get(reverse("turmas:detalhe", args=[self.turma.pk]))
        self.assertEqual(resposta.status_code, 403)
