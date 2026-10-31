from django.db import models

from apps.turmas.models import Aluno, Turma


class Aula(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name="aulas")
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField(help_text="Texto da aula, como o professor escreveu (versão original).")
    publicada = models.BooleanField(default=False, help_text="Só aulas publicadas aparecem para os alunos.")
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return self.titulo

    def tem_respostas(self):
        return Resposta.objects.filter(questao__aula=self).exists()


class Questao(models.Model):
    """Questão de múltipla escolha. Alternativas e gabarito são sempre os do professor."""

    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="questoes")
    ordem = models.PositiveSmallIntegerField()
    enunciado = models.TextField()
    alternativas = models.JSONField(help_text="Lista com o texto de cada alternativa, na ordem.")
    indice_correto = models.PositiveSmallIntegerField(help_text="Posição da alternativa correta (0 = primeira).")

    class Meta:
        ordering = ["ordem"]
        constraints = [models.UniqueConstraint(fields=["aula", "ordem"], name="questao_ordem_unica_na_aula")]

    def __str__(self):
        return f"{self.aula} — questão {self.ordem}"


class Resposta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="respostas")
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="respostas")
    indice_escolhido = models.PositiveSmallIntegerField()
    correta = models.BooleanField()
    tempo_ms = models.PositiveIntegerField(
        null=True, blank=True, help_text="Tempo entre abrir a aula e enviar as respostas, em milissegundos."
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["aluno", "questao"], name="uma_resposta_por_questao")]

    def __str__(self):
        return f"{self.aluno} — {self.questao}"
