from django.test import TestCase
from django.urls import reverse

from apps.contas.models import Usuario

SENHA = "senha-de-teste-123"


def criar_usuario(username, papel):
    return Usuario.objects.create_user(username=username, password=SENHA, papel=papel)


class LoginTests(TestCase):
    def test_visitante_sem_login_vai_para_tela_de_entrar(self):
        resposta = self.client.get(reverse("contas:inicio"))
        self.assertRedirects(resposta, reverse("contas:entrar") + "?next=/")

    def test_cada_papel_cai_na_sua_pagina_inicial(self):
        casos = [
            ("prof", Usuario.Papel.PROFESSOR, "painel:inicio"),
            ("familia", Usuario.Papel.FAMILIA, "perfis:inicio"),
            ("aluno", Usuario.Papel.ALUNO, "aulas:inicio"),
        ]
        for username, papel, destino in casos:
            with self.subTest(papel=papel):
                criar_usuario(username, papel)
                resposta = self.client.post(
                    reverse("contas:entrar"), {"username": username, "password": SENHA}, follow=True
                )
                self.assertRedirects(resposta, reverse(destino))
                self.client.post(reverse("contas:sair"))

    def test_senha_errada_nao_entra(self):
        criar_usuario("prof", Usuario.Papel.PROFESSOR)
        resposta = self.client.post(reverse("contas:entrar"), {"username": "prof", "password": "errada"})
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(resposta.wsgi_request.user.is_authenticated)

    def test_aluno_nao_acessa_pagina_do_professor(self):
        criar_usuario("aluno", Usuario.Papel.ALUNO)
        self.client.login(username="aluno", password=SENHA)
        resposta = self.client.get(reverse("painel:inicio"))
        self.assertEqual(resposta.status_code, 403)

    def test_sair_encerra_a_sessao(self):
        criar_usuario("prof", Usuario.Papel.PROFESSOR)
        self.client.login(username="prof", password=SENHA)
        resposta = self.client.post(reverse("contas:sair"))
        self.assertRedirects(resposta, reverse("contas:entrar"))
        self.assertRedirects(self.client.get(reverse("painel:inicio")), reverse("contas:entrar") + "?next=/professor/")
