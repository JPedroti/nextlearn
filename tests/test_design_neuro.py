"""Regras da skill design-neuro (.claude/skills/design-neuro/SKILL.md) aplicadas às telas reais."""

import re
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from apps.aulas.models import Aula, Questao, Resposta
from apps.contas.models import Usuario
from apps.perfis.models import Perfil
from apps.turmas.models import Aluno, Turma

SENHA = "senha-de-teste-123"
CSS_TEMAS = Path(settings.BASE_DIR) / "static" / "css" / "temas.css"


def luminancia(cor):
    r, g, b = (int(cor.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4))
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in (r, g, b)]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contraste(cor_a, cor_b):
    clara, escura = sorted([luminancia(cor_a), luminancia(cor_b)], reverse=True)
    return (clara + 0.05) / (escura + 0.05)


def temas_do_css():
    """{nome do tema: {variável: cor}} lido de static/css/temas.css (blocos body.tema-* e body.modo-limpo)."""
    texto = CSS_TEMAS.read_text(encoding="utf-8")
    temas = {}
    for nome, corpo in re.findall(r"body\.(tema-\w+|modo-limpo)\s*\{([^}]*)\}", texto):
        cores = dict(re.findall(r"--([\w-]+):\s*(#[0-9A-Fa-f]{6})", corpo))
        if cores:
            temas[nome] = cores
    return temas


class ContrasteTests(SimpleTestCase):
    """Todo par de texto com pelo menos 4,5:1 (WCAG 2.2), calculado pela luminância relativa, não de olho."""

    PARES = [
        ("texto", "fundo"), ("texto", "superficie"), ("texto-suave", "fundo"), ("texto-suave", "superficie"),
        ("destaque", "superficie"), ("destaque", "fundo"), ("destaque", "destaque-suave"),
    ]

    def test_os_cinco_temas_existem(self):
        self.assertEqual(
            set(temas_do_css()), {"tema-base", "tema-foco", "tema-textual", "tema-concreto", "modo-limpo"}
        )

    def test_todos_os_pares_de_texto_passam_de_4_5(self):
        for nome, cores in temas_do_css().items():
            for texto, fundo in self.PARES:
                with self.subTest(tema=nome, par=f"{texto}/{fundo}"):
                    self.assertGreaterEqual(contraste(cores[texto], cores[fundo]), 4.5)
            with self.subTest(tema=nome, par="branco/destaque"):
                self.assertGreaterEqual(contraste("#FFFFFF", cores["destaque"]), 4.5)


class TemaDaTelaTests(TestCase):
    def setUp(self):
        self.professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=self.professor)

    def classes_do_body(self, resposta):
        return re.search(r'<body class="([^"]*)"', resposta.content.decode()).group(1).split()

    def entrar_como_aluno(self, username="ana", **apoios):
        usuario = Usuario.objects.create_user(username, password=SENHA, papel=Usuario.Papel.ALUNO)
        aluno = Aluno.objects.create(usuario=usuario, turma=self.turma)
        Perfil.objects.create(aluno=aluno, **apoios)
        self.client.login(username=username, password=SENHA)
        return aluno

    def test_tema_segue_o_apoio_mais_restritivo(self):
        casos = [
            ({}, "tema-base", []),
            ({"concreto": True}, "tema-concreto", ["apoio-concreto"]),
            ({"textual": True}, "tema-textual", ["apoio-textual"]),
            ({"foco": True}, "tema-foco", ["apoio-foco"]),
            ({"foco": True, "textual": True}, "tema-foco", ["apoio-foco", "apoio-textual"]),
            ({"foco": True, "textual": True, "concreto": True}, "tema-foco", ["apoio-foco", "apoio-textual", "apoio-concreto"]),
        ]
        for i, (apoios, tema, classes_de_apoio) in enumerate(casos):
            with self.subTest(apoios=apoios):
                self.entrar_como_aluno(f"aluno{i}", **apoios)
                classes = self.classes_do_body(self.client.get(reverse("aulas:inicio")))
                self.assertIn(tema, classes)
                self.assertEqual([c for c in classes if c.startswith("apoio-")], classes_de_apoio)

    def test_modo_limpo_e_letras_espacadas_viram_classes_do_body(self):
        self.entrar_como_aluno(foco=True, modo_limpo=True, fonte_dislexia=True)
        classes = self.classes_do_body(self.client.get(reverse("aulas:inicio")))
        self.assertTrue({"tema-foco", "modo-limpo", "fonte-dislexia"} <= set(classes))

    def test_professor_usa_o_tema_base(self):
        self.client.login(username="prof", password=SENHA)
        self.assertIn("tema-base", self.classes_do_body(self.client.get(reverse("painel:inicio"))))

    def test_barra_usa_letras_espacadas_e_nenhum_emoji(self):
        self.entrar_como_aluno()
        resposta = self.client.get(reverse("aulas:inicio"))
        self.assertContains(resposta, "Letras espaçadas")
        self.assertNotContains(resposta, "Fonte para dislexia")
        for emoji in ("🔤", "🔊", "☀"):
            self.assertNotContains(resposta, emoji)


class TelasDoAlunoTests(TestCase):
    def setUp(self):
        professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        self.turma = Turma.objects.create(nome="6º A", professor=professor)
        usuario = Usuario.objects.create_user("ana", password=SENHA, papel=Usuario.Papel.ALUNO)
        self.aluno = Aluno.objects.create(usuario=usuario, turma=self.turma)
        self.perfil = Perfil.objects.create(aluno=self.aluno, foco=True)
        self.client.login(username="ana", password=SENHA)

    def criar_aula(self, titulo):
        aula = Aula.objects.create(turma=self.turma, titulo=titulo, conteudo="Texto.", publicada=True)
        Questao.objects.create(aula=aula, ordem=1, enunciado="Q1", alternativas=["a", "b"], indice_correto=1)
        return aula

    def test_correcao_diz_certo_ou_errado_por_escrito(self):
        aula = self.criar_aula("Frações")
        questao = aula.questoes.get()
        Resposta.objects.create(aluno=self.aluno, questao=questao, indice_escolhido=0, correta=False)
        resposta = self.client.get(reverse("aulas:ver", args=[aula.pk]))
        self.assertContains(resposta, "Ainda não. A resposta certa é a B.")
        Resposta.objects.filter(aluno=self.aluno).update(indice_escolhido=1, correta=True)
        self.assertContains(self.client.get(reverse("aulas:ver", args=[aula.pk])), "✓ Certo!")

    def test_com_foco_a_proxima_aula_vem_em_destaque_e_as_outras_recolhidas(self):
        self.criar_aula("Primeira")
        self.criar_aula("Segunda")
        resposta = self.client.get(reverse("aulas:inicio"))
        self.assertContains(resposta, "Sua próxima aula")
        self.assertContains(resposta, "Outras aulas (1)")

    def test_sem_foco_a_lista_aparece_inteira(self):
        self.perfil.foco = False
        self.perfil.save()
        self.criar_aula("Primeira")
        self.criar_aula("Segunda")
        resposta = self.client.get(reverse("aulas:inicio"))
        self.assertNotContains(resposta, "Sua próxima aula")
        self.assertContains(resposta, "Primeira")
        self.assertContains(resposta, "Segunda")


class DicasParaAFamiliaTests(TestCase):
    def test_relatorio_mostra_dicas_dos_apoios_que_o_professor_ligou(self):
        professor = Usuario.objects.create_user("prof", password=SENHA, papel=Usuario.Papel.PROFESSOR)
        familia = Usuario.objects.create_user("mae", password=SENHA, papel=Usuario.Papel.FAMILIA)
        turma = Turma.objects.create(nome="6º A", professor=professor)
        usuario = Usuario.objects.create_user("ana", password=SENHA, papel=Usuario.Papel.ALUNO)
        aluno = Aluno.objects.create(usuario=usuario, turma=turma, responsavel=familia)
        Perfil.objects.create(aluno=aluno, concreto=True)
        self.client.login(username="mae", password=SENHA)
        resposta = self.client.get(reverse("perfis:relatorio", args=[aluno.pk]))
        self.assertContains(resposta, "Como ajudar em casa")
        self.assertContains(resposta, "dividir uma pizza")
        self.assertNotContains(resposta, "Divida a lição de casa")  # foco não está ligado
