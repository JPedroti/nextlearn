from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula, EventoUso, Questao
from apps.contas.models import Usuario
from apps.perfis.models import Perfil
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"


class PreferenciasTests(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        usuario = Usuario.objects.create_user("ana", password=SENHA, papel=Usuario.Papel.ALUNO)
        self.aluno = Aluno.objects.create(usuario=usuario, turma=self.turma)
        self.perfil = Perfil.objects.create(aluno=self.aluno)
        self.aula = Aula.objects.create(turma=self.turma, titulo="Frações", conteudo="Texto", publicada=True)
        Questao.objects.create(aula=self.aula, ordem=1, enunciado="?", alternativas=["a", "b"], indice_correto=0)
        self.url = reverse("perfis:alternar_preferencia")
        self.client.login(username="ana", password=SENHA)

    def alternar(self, campo, valor, **extra):
        dados = {"campo": campo, "valor": "1" if valor else "0", "aula": str(self.aula.pk)}
        return self.client.post(self.url, dados, **extra)

    def classes_do_body(self):
        html = self.client.get(reverse("aulas:ver", args=[self.aula.pk])).content.decode()
        inicio = html.index("<body")
        return html[inicio:html.index(">", inicio)]

    def test_ligar_registra_evento_com_a_aula(self):
        self.alternar("leitura_voz", True)
        evento = EventoUso.objects.get()
        self.assertEqual((evento.aluno, evento.aula, evento.tipo), (self.aluno, self.aula, "ativou_leitura_voz"))

    def test_desligar_nao_registra_evento(self):
        self.alternar("modo_limpo", False)
        self.assertFalse(EventoUso.objects.exists())

    def test_escolha_vale_na_sessao_por_cima_do_perfil(self):
        self.perfil.fonte_dislexia = True  # o professor deixou ligada
        self.perfil.save()
        self.assertIn("fonte-dislexia", self.classes_do_body())
        self.alternar("fonte_dislexia", False)
        self.assertNotIn("fonte-dislexia", self.classes_do_body())
        # A escolha do aluno não muda o perfil: isso é com o professor.
        self.perfil.refresh_from_db()
        self.assertTrue(self.perfil.fonte_dislexia)

    def test_pedido_por_javascript_recebe_json(self):
        resposta = self.alternar("modo_limpo", True, HTTP_X_REQUESTED_WITH="fetch")
        self.assertEqual(resposta.json(), {"campo": "modo_limpo", "valor": True})

    def test_sem_javascript_volta_para_a_pagina(self):
        destino = reverse("aulas:ver", args=[self.aula.pk])
        resposta = self.client.post(self.url, {"campo": "modo_limpo", "valor": "1", "next": destino})
        self.assertRedirects(resposta, destino)

    def test_campo_desconhecido_e_recusado(self):
        resposta = self.client.post(self.url, {"campo": "foco", "valor": "1"})
        self.assertEqual(resposta.status_code, 400)
        self.assertFalse(EventoUso.objects.exists())

    def test_aula_de_outra_turma_nao_entra_no_evento(self):
        outra = Turma.objects.create(nome="Outra", professor=self.professor)
        aula_alheia = Aula.objects.create(turma=outra, titulo="X", conteudo="Y", publicada=True)
        self.client.post(self.url, {"campo": "leitura_voz", "valor": "1", "aula": str(aula_alheia.pk)})
        self.assertIsNone(EventoUso.objects.get().aula)

    def test_barra_e_botoes_de_ouvir_aparecem_para_o_aluno(self):
        resposta = self.client.get(reverse("aulas:ver", args=[self.aula.pk]))
        self.assertContains(resposta, "Apoios de leitura:")
        self.assertContains(resposta, 'data-ouvir="titulo-aula texto-aula"')
        self.assertContains(resposta, "js/leitura_voz.js")

    def test_professor_nao_ve_a_barra_nem_alterna(self):
        self.client.login(username="prof", password=SENHA)
        self.assertNotContains(self.client.get(reverse("painel:inicio")), "Apoios de leitura:")
        self.assertEqual(self.client.post(self.url, {"campo": "modo_limpo", "valor": "1"}).status_code, 403)

    def test_professor_define_o_padrao_das_preferencias(self):
        self.client.login(username="prof", password=SENHA)
        self.client.post(reverse("perfis:editar_apoios", args=[self.aluno.pk]), {"leitura_voz": "on"})
        self.perfil.refresh_from_db()
        self.assertTrue(self.perfil.leitura_voz)
        self.assertEqual(self.perfil.mascara, 0)  # preferência de tela não muda a versão da aula
