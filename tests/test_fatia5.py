from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula, EventoUso, Questao, Resposta, VersaoAdaptada
from apps.contas.models import Usuario
from apps.perfis.models import Perfil, SugestaoPerfil
from apps.perfis.sugestoes import LIMITE_DE_USOS
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"


class Fatia5Base(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        self.aula = Aula.objects.create(turma=self.turma, titulo="Frações", conteudo="Texto original", publicada=True)
        self.q1 = Questao.objects.create(aula=self.aula, ordem=1, enunciado="Q1", alternativas=["a", "b"], indice_correto=0)
        self.q2 = Questao.objects.create(aula=self.aula, ordem=2, enunciado="Q2", alternativas=["a", "b"], indice_correto=1)

    def criar_aluno(self, username, **apoios):
        usuario = Usuario.objects.create_user(username, password=SENHA, papel=Usuario.Papel.ALUNO)
        aluno = Aluno.objects.create(usuario=usuario, turma=self.turma)
        Perfil.objects.create(aluno=aluno, **apoios)
        return aluno

    def responder(self, username, escolhas):
        self.client.login(username=username, password=SENHA)
        dados = {f"questao_{q.pk}": str(i) for q, i in zip([self.q1, self.q2], escolhas)}
        self.client.post(reverse("aulas:ver", args=[self.aula.pk]), dados)


class VersaoVistaTests(Fatia5Base):
    def test_resposta_guarda_a_versao_adaptada_que_o_aluno_viu(self):
        aluno = self.criar_aluno("ana", foco=True)
        VersaoAdaptada.objects.create(aula=self.aula, mascara=4, conteudo="x", enunciados=["a", "b"], aprovada=True)
        self.responder("ana", [0, 1])
        self.assertEqual(set(Resposta.objects.filter(aluno=aluno).values_list("versao_mascara", flat=True)), {4})

    def test_sem_versao_aprovada_conta_como_original(self):
        aluno = self.criar_aluno("ana", foco=True)
        VersaoAdaptada.objects.create(aula=self.aula, mascara=4, conteudo="x", enunciados=["a", "b"], aprovada=False)
        self.responder("ana", [0, 1])
        self.assertEqual(set(Resposta.objects.filter(aluno=aluno).values_list("versao_mascara", flat=True)), {0})


class SugestaoPeloUsoTests(Fatia5Base):
    def setUp(self):
        super().setUp()
        self.aluno = self.criar_aluno("ana")
        self.client.login(username="ana", password=SENHA)

    def ligar(self, campo="leitura_voz", vezes=1):
        for _ in range(vezes):
            self.client.post(reverse("perfis:alternar_preferencia"), {"campo": campo, "valor": "1"})

    def test_sugere_depois_do_limite_de_usos(self):
        self.ligar(vezes=LIMITE_DE_USOS - 1)
        self.assertFalse(SugestaoPerfil.objects.exists())
        self.ligar()
        sugestao = SugestaoPerfil.objects.get()
        self.assertEqual((sugestao.campo, sugestao.valor_sugerido, sugestao.origem), ("leitura_voz", True, "uso"))
        self.assertIn(f"{LIMITE_DE_USOS} vezes", sugestao.motivo)

    def test_nao_repete_sugestao_pendente_nem_recusada(self):
        self.ligar(vezes=LIMITE_DE_USOS + 2)
        self.assertEqual(SugestaoPerfil.objects.count(), 1)
        SugestaoPerfil.objects.update(status="recusada")
        self.ligar(vezes=3)
        self.assertEqual(SugestaoPerfil.objects.count(), 1)

    def test_nao_sugere_o_que_ja_vem_ligado(self):
        self.aluno.perfil.leitura_voz = True
        self.aluno.perfil.save()
        self.ligar(vezes=LIMITE_DE_USOS)
        self.assertFalse(SugestaoPerfil.objects.exists())

    def test_aceitar_liga_a_preferencia_no_perfil(self):
        self.ligar(vezes=LIMITE_DE_USOS)
        sugestao = SugestaoPerfil.objects.get()
        self.client.login(username="prof", password=SENHA)
        painel = reverse("painel:turma", args=[self.turma.pk])
        resposta = self.client.post(reverse("perfis:aceitar_sugestao", args=[sugestao.pk]), {"next": painel})
        self.assertRedirects(resposta, painel)
        self.aluno.perfil.refresh_from_db()
        self.assertTrue(self.aluno.perfil.leitura_voz)


class PainelTests(Fatia5Base):
    def setUp(self):
        super().setUp()
        self.ana = self.criar_aluno("ana", foco=True)
        self.bia = self.criar_aluno("bia")
        self.caio = self.criar_aluno("caio")  # não responde
        VersaoAdaptada.objects.create(aula=self.aula, mascara=4, conteudo="x", enunciados=["a", "b"], aprovada=True)
        self.responder("ana", [0, 1])  # 2 acertos, versão adaptada
        self.responder("bia", [0, 0])  # 1 acerto, original
        EventoUso.objects.create(aluno=self.bia, aula=self.aula, tipo="ativou_fonte_dislexia")
        self.client.login(username="prof", password=SENHA)
        self.url = reverse("painel:turma", args=[self.turma.pk])

    def test_numeros_por_aluno(self):
        linhas = {l["aluno"].usuario.username: l for l in self.client.get(self.url).context["linhas_alunos"]}
        self.assertEqual(linhas["ana"]["placar"], {"acertos": 2, "total": 2, "pct": 100})
        self.assertEqual(linhas["ana"]["aulas_com_versao_adaptada"], 1)
        self.assertEqual(linhas["bia"]["placar"]["pct"], 50)
        self.assertEqual(linhas["bia"]["usos"], [{"rotulo": "Fonte para dislexia", "vezes": 1}])
        self.assertEqual(linhas["caio"]["placar"]["total"], 0)

    def test_numeros_por_aula_e_por_questao(self):
        linha = self.client.get(self.url).context["linhas_aulas"][0]
        self.assertEqual(linha["alunos_responderam"], 2)
        self.assertEqual(linha["placar"], {"acertos": 3, "total": 4, "pct": 75})
        self.assertEqual(linha["placar_adaptada"]["pct"], 100)
        self.assertEqual(linha["placar_original"]["pct"], 50)
        self.assertEqual([q["placar"]["pct"] for q in linha["questoes"]], [100, 50])

    def test_mostra_sugestoes_pendentes_da_turma(self):
        SugestaoPerfil.objects.create(aluno=self.caio, campo="modo_limpo", valor_sugerido=True, motivo="m", origem="uso")
        self.assertContains(self.client.get(self.url), "Ligar “Modo limpo”")

    def test_so_o_professor_da_turma_ve(self):
        Usuario.objects.create_user("outro", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.client.login(username="outro", password=SENHA)
        self.assertEqual(self.client.get(self.url).status_code, 404)
        self.client.login(username="ana", password=SENHA)
        self.assertEqual(self.client.get(self.url).status_code, 403)
