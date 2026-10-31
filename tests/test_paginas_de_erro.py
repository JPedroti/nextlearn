"""Páginas de erro em português, no lugar das páginas padrão do Django (em inglês)."""

from django.template.loader import render_to_string
from django.test import TestCase

from apps.contas.models import Usuario

SENHA = "senha-de-teste-123"


class PaginasDeErroTests(TestCase):
    def test_404(self):
        resposta = self.client.get("/nao-existe/")
        self.assertEqual(resposta.status_code, 404)
        self.assertContains(resposta, "Página não encontrada", status_code=404)

    def test_403_quando_o_papel_nao_combina(self):
        Usuario.objects.create_user("ana", password=SENHA, papel=Usuario.Papel.ALUNO)
        self.client.login(username="ana", password=SENHA)
        resposta = self.client.get("/professor/")
        self.assertContains(resposta, "Você não tem acesso a esta página", status_code=403)

    def test_500_nao_depende_do_banco_nem_do_login(self):
        self.assertIn("Algo deu errado do nosso lado", render_to_string("500.html"))
