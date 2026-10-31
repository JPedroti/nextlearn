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


class RecadoFamilia(models.Model):
    """Sugestão, observação ou dúvida que a família manda ao professor. O professor lê e marca como resolvido."""

    class Tipo(models.TextChoices):
        SUGESTAO = "sugestao", "Sugestão para as aulas"
        OBSERVACAO = "observacao", "Algo que notamos em casa"
        DUVIDA = "duvida", "Dúvida"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="recados_familia")
    autor = models.ForeignKey("contas.Usuario", on_delete=models.SET_NULL, null=True, related_name="recados_enviados")
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.SUGESTAO)
    texto = models.TextField(max_length=1500)
    lido = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["lido", "-criado_em"]

    def __str__(self):
        return f"{self.get_tipo_display()} sobre {self.aluno}"
