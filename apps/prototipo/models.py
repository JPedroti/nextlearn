from django.db import models

from apps.turmas.models import Aluno


class ConfigFamilia(models.Model):
    """O que a família combina para o estudo em casa (ECA Digital: supervisão parental e limite de tempo).
    Estes valores alimentam a área do aluno (limite diário, meta semanal, ofensiva visível)."""

    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name="config_familia")
    limite_diario_min = models.PositiveSmallIntegerField("Limite de estudo por dia (min)", default=40)
    meta_semanal = models.PositiveSmallIntegerField("Meta de aulas por semana", default=2)
    mostrar_ofensiva = models.BooleanField("Mostrar ofensiva semanal", default=True,
                                           help_text="Alguns alunos (ex.: com TEA) ficam ansiosos com contadores; a família pode esconder.")
    resumo_semanal = models.BooleanField("Quero o resumo semanal", default=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Combinados da família de {self.aluno}"
