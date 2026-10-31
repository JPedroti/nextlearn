"""ia/gerar_questoes.py + fluxo do professor (PDF/texto -> IA sugere -> revisa/aprova)."""

from unittest import mock

from django.test import TestCase, override_settings
from django.urls import reverse

from apps.aulas.models import Aula, Questao
from apps.contas.models import Usuario
from apps.turmas.models import Turma
from ia.gerar_questoes import ErroGeracaoQuestoes, SaidaQuestao, SaidaQuestoes, gerar_questoes

SENHA = "senha-de-teste-123"


def saida_valida():
    return SaidaQuestoes(
        titulo="Frações",
        questoes=[
            SaidaQuestao(tipo="flashcard", enunciado="O que é denominador?", resposta_referencia="O número de baixo da fração."),
            SaidaQuestao(tipo="multipla", enunciado="Em 3/4, o 4 é o quê?", alternativas=["numerador", "denominador", "resultado"], indice_correto=1),
            SaidaQuestao(tipo="escrever", enunciado="Explique o que é numerador.", resposta_referencia="O número de cima, que indica quantas partes foram consideradas."),
        ],
    )


class GerarQuestoesTests(TestCase):
    @mock.patch("ia.cliente.gerar")
    def test_gera_e_devolve_questoes_validas(self, gerar):
        gerar.return_value = saida_valida()
        saida = gerar_questoes("Uma fração tem numerador e denominador.", "Frações")
        self.assertEqual(saida.titulo, "Frações")
        self.assertEqual(len(saida.questoes), 3)
        self.assertIn("numerador", gerar.call_args.args[1])

    @mock.patch("ia.cliente.gerar")
    def test_texto_vazio_recusa(self, gerar):
        with self.assertRaises(ErroGeracaoQuestoes):
            gerar_questoes("   ")
        gerar.assert_not_called()

    @mock.patch("ia.cliente.gerar")
    def test_multipla_sem_indice_valido_recusa(self, gerar):
        gerar.return_value = SaidaQuestoes(
            titulo="A",
            questoes=[SaidaQuestao(tipo="multipla", enunciado="X?", alternativas=["a", "b"], indice_correto=9)],
        )
        with self.assertRaises(ErroGeracaoQuestoes):
            gerar_questoes("texto")

    @mock.patch("ia.cliente.gerar")
    def test_erro_da_api_vira_mensagem_amigavel(self, gerar):
        gerar.side_effect = RuntimeError("503")
        with self.assertRaises(ErroGeracaoQuestoes):
            gerar_questoes("texto")


@override_settings(GEMINI_API_KEY="chave")
class FluxoProfessorTests(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        self.client.login(username="prof", password=SENHA)

    def _chegar_a_revisao(self, gerar):
        gerar.return_value = saida_valida()
        self.client.post(reverse("aulas:gerar_questoes_via_pdf", args=[self.turma.pk]), {"texto": "Aula sobre frações."})
        return reverse("aulas:revisar_questoes", args=[self.turma.pk])

    @mock.patch("ia.cliente.gerar")
    def test_gera_com_texto_e_vai_para_revisao(self, gerar):
        gerar.return_value = saida_valida()
        resposta = self.client.post(reverse("aulas:gerar_questoes_via_pdf", args=[self.turma.pk]), {"texto": "texto"})
        self.assertRedirects(resposta, reverse("aulas:revisar_questoes", args=[self.turma.pk]))

    @mock.patch("ia.cliente.gerar")
    def test_aprova_e_salva_preservando_todos_os_tipos(self, gerar):
        self._chegar_a_revisao(gerar)
        dados = {
            "titulo": "Frações",
            "conteudo": "Aula sobre frações.",
            # Questão 0 (flashcard)
            "0_tipo": "flashcard", "0_enunciado": "O que é denominador?",
            "0_alt_a": "", "0_alt_b": "", "0_alt_c": "", "0_alt_d": "", "0_correta": "a",
            "0_resposta": "O número de baixo.",
            # Questão 1 (multipla)
            "1_tipo": "multipla", "1_enunciado": "Em 3/4, o 4 é o quê?",
            "1_alt_a": "numerador", "1_alt_b": "denominador", "1_alt_c": "resultado", "1_alt_d": "",
            "1_correta": "b", "1_resposta": "",
            # Questão 2 (escrever)
            "2_tipo": "escrever", "2_enunciado": "Explique numerador.",
            "2_alt_a": "", "2_alt_b": "", "2_alt_c": "", "2_alt_d": "", "2_correta": "a",
            "2_resposta": "O número de cima.",
        }
        resposta = self.client.post(reverse("aulas:revisar_questoes", args=[self.turma.pk]), dados)
        aula = Aula.objects.get(turma=self.turma, titulo="Frações")
        self.assertFalse(aula.publicada)  # nasce como rascunho
        self.assertRedirects(resposta, reverse("aulas:detalhe_professor", args=[aula.pk]))
        questoes = list(aula.questoes.order_by("ordem"))
        self.assertEqual([q.tipo for q in questoes], ["flashcard", "multipla", "escrever"])
        self.assertEqual(questoes[0].resposta_referencia, "O número de baixo.")
        self.assertEqual(questoes[1].alternativas, ["numerador", "denominador", "resultado"])
        self.assertEqual(questoes[1].indice_correto, 1)
        self.assertEqual(questoes[2].resposta_referencia, "O número de cima.")

    @mock.patch("ia.cliente.gerar")
    def test_ia_nao_configurada_nao_oferece_a_tela(self, gerar):
        from django.test import override_settings as _ov
        gerar.return_value = saida_valida()
        with _ov(GEMINI_API_KEY=""):
            resposta = self.client.get(reverse("aulas:gerar_questoes_via_pdf", args=[self.turma.pk]))
        self.assertRedirects(resposta, reverse("aulas:nova_via_pdf", args=[self.turma.pk]))
        gerar.assert_not_called()