from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """Usuário do Chamilion. O `papel` decide quais telas a pessoa vê."""

    class Papel(models.TextChoices):
        PROFESSOR = "professor", "Professor(a)"
        FAMILIA = "familia", "Família"
        ALUNO = "aluno", "Aluno(a)"

    papel = models.CharField(max_length=20, choices=Papel.choices)

    # O `createsuperuser` pergunta também o papel.
    REQUIRED_FIELDS = ["email", "papel"]

    def __str__(self):
        return self.get_full_name() or self.username
