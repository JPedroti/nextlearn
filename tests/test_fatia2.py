from unittest import mock

from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula, Questao, Resposta, VersaoAdaptada
from apps.contas.models import Usuario
from apps.perfis.models import Perfil, bits_da_mascara, calcular_mascara, nomes_da_mascara
from apps.turmas.models import Aluno, Turma
from ia.cliente import SaidaVersao
from ia.gerar_versao import ErroGeracao, gerar_versao
from ia.prompt_builder import ler_bloco, montar_mensagem, montar_system_prompt

SENHA = "senha-de-teste-123"


def saida_falsa(num_enunciados=2):
    return SaidaVersao(
        conteudo="Passo 1. Texto adaptado.",
        enunciados=[f"Enunciado adaptado {i + 1}" for i in range(num_enunciados)],
    )


class MascaraTests(TestCase):
    def test_calcula_as_8_mascaras(self):
        self.assertEqual(calcular_mascara(False, False, False), 0)
        self.assertEqual(calcular_mascara(False, False, True), 1)
        self.assertEqual(calcular_mascara(False, True, False), 2)
        self.assertEqual(calcular_mascara(True, False, False), 4)
        self.assertEqual(calcular_mascara(True, True, True), 7)

    def test_bits_e_mascara_sao_inversos(self):
        for mascara in range(8):
            self.assertEqual(calcular_mascara(*bits_da_mascara(mascara)), mascara)

    def test_nomes_da_mascara(self):
        self.assertEqual(nomes_da_mascara(5), ["Atenção e foco", "Interativo e concreto"])
        self.assertEqual(nomes_da_mascara(0), [])


class PromptBuilderTests(TestCase):
    def test_sem_apoios_so_tem_a_base(self):
        self.assertEqual(montar_system_prompt(False, False, False), ler_bloco("base.md"))

    def test_um_apoio_inclui_o_bloco_e_nao_inclui_conflitos(self):
        prompt = montar_system_prompt(True, False, False)
        self.assertIn(ler_bloco("foco.md"), prompt)
        self.assertNotIn(ler_bloco("textual.md"), prompt)
        self.assertNotIn(ler_bloco("conflitos.md"), prompt)

    def test_dois_apoios_incluem_conflitos(self):
        prompt = montar_system_prompt(False, True, True)
        self.assertIn(ler_bloco("textual.md"), prompt)
        self.assertIn(ler_bloco("concreto.md"), prompt)
        self.assertIn(ler_bloco("conflitos.md"), prompt)

    def test_comentarios_da_equipe_nao_vao_para_a_ia(self):
        self.assertNotIn("<!--", montar_system_prompt(True, True, True))

    def test_mensagem_tem_a_aula_e_nenhum_dado_do_aluno(self):
        professor = Usuario.objects.create_user("prof", papel=Usuario.Papel.PROFESSOR)
        turma = Turma.objects.create(nome="6º A", professor=professor)
        usuario = Usuario.objects.create_user("fulana", papel=Usuario.Papel.ALUNO, first_name="Fulana", last_name="Silva")
        Perfil.objects.create(aluno=Aluno.objects.create(usuario=usuario, turma=turma), foco=True)
        aula = Aula.objects.create(turma=turma, titulo="Frações", conteudo="Uma fração é parte de um todo.")
        Questao.objects.create(aula=aula, ordem=1, enunciado="O que é fração?", alternativas=["a", "b"], indice_correto=0)

        mensagem = montar_mensagem(aula)
        self.assertIn("<aula>", mensagem)
        self.assertIn("Uma fração é parte de um todo.", mensagem)
        self.assertIn("O que é fração?", mensagem)
        for dado_pessoal in ("Fulana", "Silva", "fulana"):
            self.assertNotIn(dado_pessoal, mensagem)


class Fatia2Base(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        self.aula = Aula.objects.create(turma=self.turma, titulo="Frações", conteudo="Texto original", publicada=True)
        self.q1 = Questao.objects.create(
            aula=self.aula, ordem=1, enunciado="Original 1", alternativas=["2", "5", "10"], indice_correto=1
        )
        self.q2 = Questao.objects.create(
            aula=self.aula, ordem=2, enunciado="Original 2", alternativas=["Sim", "Não"], indice_correto=1
        )

    def criar_aluno(self, username, **apoios):
        usuario = Usuario.objects.create_user(username, password=SENHA, papel=Usuario.Papel.ALUNO)
        aluno = Aluno.objects.create(usuario=usuario, turma=self.turma)
        Perfil.objects.create(aluno=aluno, **apoios)
        return aluno


@mock.patch("ia.cliente.gerar")
class GerarVersaoTests(Fatia2Base):
    def test_gera_e_salva_sem_aprovar(self, gerar):
        gerar.return_value = saida_falsa()
        versao = gerar_versao(self.aula, 4)
        self.assertFalse(versao.aprovada)
        self.assertEqual(versao.enunciados, ["Enunciado adaptado 1", "Enunciado adaptado 2"])
        system_prompt = gerar.call_args.args[0]
        self.assertIn(ler_bloco("foco.md"), system_prompt)

    def test_cache_nao_chama_a_ia_de_novo(self, gerar):
        gerar.return_value = saida_falsa()
        primeira = gerar_versao(self.aula, 3)
        segunda = gerar_versao(self.aula, 3)
        self.assertEqual(primeira.pk, segunda.pk)
        self.assertEqual(gerar.call_count, 1)

    def test_forcar_gera_de_novo_e_tira_a_aprovacao(self, gerar):
        gerar.return_value = saida_falsa()
        versao = gerar_versao(self.aula, 2)
        versao.aprovada = True
        versao.save()
        versao = gerar_versao(self.aula, 2, forcar=True)
        self.assertEqual(gerar.call_count, 2)
        self.assertFalse(versao.aprovada)
        self.assertEqual(VersaoAdaptada.objects.filter(aula=self.aula, mascara=2).count(), 1)

    def test_numero_errado_de_enunciados_e_recusado(self, gerar):
        gerar.return_value = saida_falsa(num_enunciados=1)
        with self.assertRaises(ErroGeracao), self.assertLogs("ia.gerar_versao", "WARNING"):
            gerar_versao(self.aula, 1)
        self.assertFalse(VersaoAdaptada.objects.exists())

    def test_erro_da_api_vira_mensagem_amigavel(self, gerar):
        gerar.side_effect = RuntimeError("503 do provedor")
        with self.assertRaises(ErroGeracao), self.assertLogs("ia.gerar_versao", "ERROR"):
            gerar_versao(self.aula, 1)

    def test_mascara_zero_nao_chama_a_ia(self, gerar):
        with self.assertRaises(ValueError):
            gerar_versao(self.aula, 0)
        gerar.assert_not_called()

    def test_gabarito_e_alternativas_nao_mudam(self, gerar):
        gerar.return_value = saida_falsa()
        gerar_versao(self.aula, 7)
        self.q1.refresh_from_db()
        self.q2.refresh_from_db()
        self.assertEqual((self.q1.enunciado, self.q1.alternativas, self.q1.indice_correto), ("Original 1", ["2", "5", "10"], 1))
        self.assertEqual((self.q2.enunciado, self.q2.alternativas, self.q2.indice_correto), ("Original 2", ["Sim", "Não"], 1))


@mock.patch("ia.cliente.gerar")
class ProfessorVersaoTests(Fatia2Base):
    def setUp(self):
        super().setUp()
        self.client.login(username="prof", password=SENHA)

    def test_marca_apoios_do_aluno(self, gerar):
        aluno = self.criar_aluno("ana")
        self.client.post(reverse("perfis:editar_apoios", args=[aluno.pk]), {"foco": "on", "concreto": "on"})
        aluno.perfil.refresh_from_db()
        self.assertEqual(aluno.perfil.mascara, 5)
        self.assertTrue(aluno.perfil.revisado_pelo_professor)

    def test_aluno_novo_ja_tem_perfil_sem_apoios(self, gerar):
        self.client.post(
            reverse("turmas:novo_aluno", args=[self.turma.pk]),
            {"first_name": "Bia", "username": "bia", "password1": SENHA, "password2": SENHA},
        )
        self.assertEqual(Perfil.objects.get(aluno__usuario__username="bia").mascara, 0)

    def test_tela_da_aula_lista_as_mascaras_da_turma(self, gerar):
        self.criar_aluno("ana", foco=True)
        self.criar_aluno("bia", foco=True)
        self.criar_aluno("caio", textual=True, concreto=True)
        self.criar_aluno("duda")  # sem apoios: aula original
        resposta = self.client.get(reverse("aulas:detalhe_professor", args=[self.aula.pk]))
        self.assertEqual([linha["mascara"] for linha in resposta.context["linhas_versoes"]], [3, 4])
        self.assertEqual(resposta.context["linhas_versoes"][1]["num_alunos"], 2)

    def test_gerar_e_aprovar_com_correcao(self, gerar):
        gerar.return_value = saida_falsa()
        resposta = self.client.post(reverse("aulas:gerar_versao", args=[self.aula.pk, 4]))
        self.assertRedirects(resposta, reverse("aulas:revisar_versao", args=[self.aula.pk, 4]))

        self.client.post(
            reverse("aulas:revisar_versao", args=[self.aula.pk, 4]),
            {"conteudo": "Texto corrigido pelo professor", "enunciado_0": "E1", "enunciado_1": "E2"},
        )
        versao = VersaoAdaptada.objects.get(aula=self.aula, mascara=4)
        self.assertTrue(versao.aprovada)
        self.assertEqual(versao.conteudo, "Texto corrigido pelo professor")
        self.assertEqual(versao.enunciados, ["E1", "E2"])

    def test_falha_da_ia_mostra_mensagem(self, gerar):
        gerar.side_effect = RuntimeError("timeout")
        with self.assertLogs("ia.gerar_versao", "ERROR"):
            resposta = self.client.post(reverse("aulas:gerar_versao", args=[self.aula.pk, 4]), follow=True)
        self.assertContains(resposta, "Tente de novo")
        self.assertFalse(VersaoAdaptada.objects.exists())

    def test_editar_aula_apaga_versoes(self, gerar):
        VersaoAdaptada.objects.create(aula=self.aula, mascara=4, conteudo="x", enunciados=["a", "b"], aprovada=True)
        dados = {
            "titulo": "Frações", "conteudo": "Texto novo",
            "questoes-TOTAL_FORMS": "2", "questoes-INITIAL_FORMS": "2",
            "questoes-MIN_NUM_FORMS": "1", "questoes-MAX_NUM_FORMS": "1000",
            "questoes-0-id": str(self.q1.pk), "questoes-0-enunciado": "Original 1",
            "questoes-0-alternativa_a": "2", "questoes-0-alternativa_b": "5", "questoes-0-alternativa_c": "10",
            "questoes-0-correta": "B",
            "questoes-1-id": str(self.q2.pk), "questoes-1-enunciado": "Original 2",
            "questoes-1-alternativa_a": "Sim", "questoes-1-alternativa_b": "Não", "questoes-1-correta": "B",
        }
        self.client.post(reverse("aulas:editar", args=[self.aula.pk]), dados)
        self.aula.refresh_from_db()
        self.assertEqual(self.aula.conteudo, "Texto novo")
        self.assertFalse(VersaoAdaptada.objects.exists())

    def test_outro_professor_nao_gera(self, gerar):
        Usuario.objects.create_user("outro", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.client.login(username="outro", password=SENHA)
        resposta = self.client.post(reverse("aulas:gerar_versao", args=[self.aula.pk, 4]))
        self.assertEqual(resposta.status_code, 404)
        gerar.assert_not_called()


class AlunoVersaoTests(Fatia2Base):
    def setUp(self):
        super().setUp()
        self.aluno = self.criar_aluno("ana", foco=True)  # máscara 4
        self.versao = VersaoAdaptada.objects.create(
            aula=self.aula, mascara=4, conteudo="Passo 1. Texto adaptado.", enunciados=["Adaptado 1", "Adaptado 2"]
        )
        self.client.login(username="ana", password=SENHA)
        self.url = reverse("aulas:ver", args=[self.aula.pk])

    def test_ve_a_original_enquanto_nao_aprovada(self):
        resposta = self.client.get(self.url)
        self.assertContains(resposta, "Texto original")
        self.assertNotContains(resposta, "Texto adaptado")

    def test_ve_a_versao_da_sua_mascara_depois_de_aprovada(self):
        self.versao.aprovada = True
        self.versao.save()
        resposta = self.client.get(self.url)
        self.assertContains(resposta, "Texto adaptado")
        self.assertContains(resposta, "Adaptado 1")
        self.assertNotContains(resposta, "Original 1")
        # Alternativas continuam as do professor
        self.assertContains(resposta, "C) 10")

    def test_aluno_sem_apoios_ve_a_original(self):
        self.versao.aprovada = True
        self.versao.save()
        self.criar_aluno("bia")
        self.client.login(username="bia", password=SENHA)
        self.assertContains(self.client.get(self.url), "Texto original")

    def test_correcao_usa_gabarito_do_professor_na_versao_adaptada(self):
        self.versao.aprovada = True
        self.versao.save()
        self.client.post(self.url, {f"questao_{self.q1.pk}": "1", f"questao_{self.q2.pk}": "0"})
        self.assertTrue(Resposta.objects.get(questao=self.q1).correta)
        self.assertFalse(Resposta.objects.get(questao=self.q2).correta)
