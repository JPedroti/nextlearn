"""Cria contas de TESTE locais (professor, aluno e família) para experimentar o login.

Uso: python manage.py contas_teste

- Só para a máquina de desenvolvimento: as senhas são geradas na hora e gravadas em
  contas_teste_local.txt (ignorado pelo Git). Não use na demo oficial.
- Rodar de novo gera senhas novas para as mesmas contas.
"""

import secrets
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.aulas.models import Aula, Questao
from apps.contas.models import Usuario
from apps.perfis.models import Perfil
from apps.turmas.models import Aluno, Turma

ARQUIVO = Path(settings.BASE_DIR) / "contas_teste_local.txt"


class Command(BaseCommand):
    help = "Cria contas de teste locais (professor, aluno, família) e uma aula publicada."

    def _usuario(self, username, papel, nome):
        usuario, _ = Usuario.objects.get_or_create(username=username, defaults={"papel": papel, "first_name": nome})
        usuario.papel = papel
        senha = secrets.token_urlsafe(9)
        usuario.set_password(senha)
        usuario.save()
        return usuario, senha

    @transaction.atomic
    def handle(self, *args, **opcoes):
        prof, s_prof = self._usuario("prof.teste", Usuario.Papel.PROFESSOR, "Professora Teste")
        aluno_u, s_aluno = self._usuario("aluno.teste", Usuario.Papel.ALUNO, "Aluno Teste")
        familia, s_fam = self._usuario("familia.teste", Usuario.Papel.FAMILIA, "Família Teste")

        turma, _ = Turma.objects.get_or_create(nome="Turma de teste (local)", professor=prof)
        aluno, _ = Aluno.objects.get_or_create(usuario=aluno_u, defaults={"turma": turma})
        aluno.turma, aluno.responsavel = turma, familia
        aluno.save()
        Perfil.objects.get_or_create(aluno=aluno)

        aula, criada = Aula.objects.get_or_create(
            turma=turma,
            titulo="Aula de teste: frações",
            defaults={
                "conteudo": "Uma fração mostra partes de um todo. Em 3/4, o 4 diz em quantas partes iguais o todo foi "
                "dividido e o 3 diz quantas partes foram pegas.",
                "publicada": True,
            },
        )
        if criada:
            Questao.objects.create(aula=aula, ordem=1, enunciado="Em 3/4, quantas partes foram pegas?",
                                   alternativas=["4", "3", "7", "1"], indice_correto=1)
            Questao.objects.create(aula=aula, ordem=2, enunciado="Uma pizza em 8 fatias iguais: 1 fatia é que fração?",
                                   alternativas=["1/8", "8/1", "1/4", "8/8"], indice_correto=0)

        ARQUIVO.write_text(
            "Contas de TESTE locais (não versionar, não usar na demo oficial)\n"
            "Login: http://127.0.0.1:8000/prototipo/login/\n\n"
            f"professor  usuario: prof.teste     senha: {s_prof}\n"
            f"aluno      usuario: aluno.teste    senha: {s_aluno}\n"
            f"familia    usuario: familia.teste  senha: {s_fam}\n",
            encoding="utf-8",
        )
        self.stdout.write(self.style.SUCCESS(f"Contas de teste prontas. Usuários e senhas em {ARQUIVO.name}"))
