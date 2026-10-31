from django.conf import settings
from django.db import models


class Turma(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="turmas",
        limit_choices_to={"papel": "professor"},
    )
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Aluno(models.Model):
    """Liga o usuário (papel aluno) à sua turma e, opcionalmente, à família responsável."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="aluno",
        limit_choices_to={"papel": "aluno"},
    )
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="alunos")
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dependentes",
        limit_choices_to={"papel": "familia"},
    )

    class Meta:
        ordering = ["usuario__first_name", "usuario__last_name"]

    def __str__(self):
        return str(self.usuario)
