"""Nova aula a partir de um PDF: o texto vira o rascunho da tela "Nova aula", que salva a aula normalmente."""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.aulas.models import Aula
from apps.contas.models import Usuario
from apps.turmas.models import Turma

SENHA = "senha-de-teste-123"


def pdf_com_texto(*linhas):
    """Monta um PDF de uma página com as linhas dadas (só letras sem acento, fonte Helvetica)."""
    texto = " ".join(f"({linha}) Tj T*" for linha in linhas)
    conteudo = f"BT /F1 12 Tf 14 TL 72 720 Td {texto} ET".encode()
    objetos = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n" % len(conteudo) + conteudo + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    pdf = b"%PDF-1.4\n"
    posicoes = []
    for numero, objeto in enumerate(objetos, start=1):
        posicoes.append(len(pdf))
        pdf += b"%d 0 obj\n" % numero + objeto + b"\nendobj\n"
    inicio_xref = len(pdf)
    pdf += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objetos) + 1)
    pdf += b"".join(b"%010d 00000 n \n" % posicao for posicao in posicoes)
    pdf += b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objetos) + 1, inicio_xref)
    return pdf


class NovaAulaViaPdfTests(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)
        self.url = reverse("aulas:nova_via_pdf", args=[self.turma.pk])
        self.client.login(username="prof", password=SENHA)

    def enviar(self, nome, conteudo):
        return self.client.post(self.url, {"pdf": SimpleUploadedFile(nome, conteudo, content_type="application/pdf")})

    def test_pagina_abre(self):
        self.assertContains(self.client.get(self.url), "Criar aula a partir de um PDF")

    def test_texto_do_pdf_preenche_a_nova_aula_e_o_formulario_salva_pela_tela_normal(self):
        resposta = self.enviar("aula.pdf", pdf_com_texto("Fracoes", "Uma fracao e parte de um todo."))
        self.assertTemplateUsed(resposta, "aulas/form_aula.html")
        form = resposta.context["form"]
        self.assertEqual(form.initial["titulo"], "Fracoes")
        self.assertIn("Uma fracao e parte de um todo.", form.initial["conteudo"])
        self.assertContains(resposta, f'action="{reverse("aulas:nova", args=[self.turma.pk])}"')
        self.assertFalse(Aula.objects.exists())  # nada é salvo antes de o professor revisar e escrever as questões

    def test_arquivo_que_nao_e_pdf(self):
        resposta = self.enviar("notas.txt", b"texto qualquer")
        self.assertTemplateUsed(resposta, "aulas/upload_pdf.html")
        self.assertContains(resposta, "Envie um arquivo PDF.")

    def test_pdf_corrompido(self):
        with self.assertLogs(level="WARNING"):  # o erro fica no log do servidor; o professor vê a mensagem simples
            resposta = self.enviar("aula.pdf", b"isto nao e um pdf")
        self.assertContains(resposta, "Não foi possível ler este arquivo como PDF.")

    def test_pdf_sem_texto(self):
        resposta = self.enviar("digitalizado.pdf", pdf_com_texto())
        self.assertContains(resposta, "não tem texto que dê para copiar")

    def test_envio_sem_arquivo(self):
        self.assertContains(self.client.post(self.url), "Escolha um arquivo PDF.")

    def test_so_o_professor_da_turma(self):
        Usuario.objects.create_user("outro", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.client.login(username="outro", password=SENHA)
        self.assertEqual(self.client.get(self.url).status_code, 404)
