"""ia/cliente.py: escolha do provedor (Gemini ou compatível com a OpenAI) e leitura do JSON. A IA é simulada."""

from unittest import mock

from django.test import SimpleTestCase, override_settings

from ia import cliente


class ConfiguradoTests(SimpleTestCase):
    @override_settings(IA_PROVEDOR="gemini", GEMINI_API_KEY="", IA_API_KEY="outra")
    def test_gemini_sem_chave(self):
        self.assertFalse(cliente.configurado())

    @override_settings(IA_PROVEDOR="gemini", GEMINI_API_KEY="chave")
    def test_gemini_com_chave(self):
        self.assertTrue(cliente.configurado())

    @override_settings(IA_PROVEDOR="openai", IA_API_KEY="", GEMINI_API_KEY="chave")
    def test_openai_usa_a_propria_chave(self):
        self.assertFalse(cliente.configurado())

    @override_settings(IA_PROVEDOR="gemini", GEMINI_API_KEY="")
    def test_gerar_sem_chave_avisa(self):
        with self.assertRaises(RuntimeError):
            cliente.gerar("sistema", "aula")


@override_settings(IA_PROVEDOR="gemini", GEMINI_API_KEY="chave", GEMINI_MODEL="modelo-flash")
class GeminiTests(SimpleTestCase):
    def test_envia_o_system_prompt_e_a_aula(self):
        saida = cliente.SaidaVersao(conteudo="Texto", enunciados=["E1"])
        with mock.patch("google.genai.Client") as Client:
            Client.return_value.models.generate_content.return_value = mock.Mock(parsed=saida)
            self.assertEqual(cliente.gerar("SISTEMA", "AULA"), saida)
        Client.assert_called_once_with(api_key="chave")
        chamada = Client.return_value.models.generate_content.call_args.kwargs
        self.assertEqual((chamada["model"], chamada["contents"]), ("modelo-flash", "AULA"))
        self.assertEqual(chamada["config"].system_instruction, "SISTEMA")


@override_settings(IA_PROVEDOR="openai", IA_API_KEY="chave", IA_BASE_URL="https://exemplo.invalid/v1", IA_MODEL="modelo")
class OpenAICompativelTests(SimpleTestCase):
    def simular(self, conteudo):
        resposta = mock.Mock()
        resposta.choices = [mock.Mock(message=mock.Mock(content=conteudo))]
        patch = mock.patch("openai.OpenAI")
        OpenAI = patch.start()
        self.addCleanup(patch.stop)
        OpenAI.return_value.chat.completions.create.return_value = resposta
        return OpenAI

    def test_envia_system_e_aula_e_le_o_json(self):
        OpenAI = self.simular('{"conteudo": "Texto", "enunciados": ["E1", "E2"]}')
        saida = cliente.gerar("SISTEMA", "AULA")
        self.assertEqual(saida, cliente.SaidaVersao(conteudo="Texto", enunciados=["E1", "E2"]))
        OpenAI.assert_called_once_with(api_key="chave", base_url="https://exemplo.invalid/v1")
        chamada = OpenAI.return_value.chat.completions.create.call_args.kwargs
        self.assertEqual(chamada["model"], "modelo")
        self.assertEqual(
            chamada["messages"], [{"role": "system", "content": "SISTEMA"}, {"role": "user", "content": "AULA"}]
        )

    def test_resposta_fora_do_formato_vira_erro(self):
        self.simular("isto não é JSON")
        with self.assertLogs("ia.cliente", "WARNING"), self.assertRaises(RuntimeError):
            cliente.gerar("SISTEMA", "AULA")
