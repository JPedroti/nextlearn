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


class VersaoAdaptada(models.Model):
    """Texto e enunciados reescritos pela IA para uma máscara de apoios (1–7).

    A restrição única (aula, mascara) é o cache: cada combinação é gerada uma vez por aula.
    Alternativas e gabarito não ficam aqui; continuam sempre os de `Questao`.
    """

    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="versoes")
    mascara = models.PositiveSmallIntegerField()
    conteudo = models.TextField()
    enunciados = models.JSONField(help_text="Um enunciado por questão, na mesma ordem das questões.")
    aprovada = models.BooleanField(default=False, help_text="Só versões aprovadas pelo professor chegam aos alunos.")
    gerada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["mascara"]
        constraints = [models.UniqueConstraint(fields=["aula", "mascara"], name="uma_versao_por_mascara")]

    def __str__(self):
        return f"{self.aula} — máscara {self.mascara:03b}"


class Resposta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="respostas")
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE, related_name="respostas")
    indice_escolhido = models.PositiveSmallIntegerField()
    correta = models.BooleanField()
    tempo_ms = models.PositiveIntegerField(
        null=True, blank=True, help_text="Tempo entre abrir a aula e enviar as respostas, em milissegundos."
    )
    versao_mascara = models.PositiveSmallIntegerField(
        default=0, help_text="Máscara da versão que o aluno viu ao responder (0 = aula original)."
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["aluno", "questao"], name="uma_resposta_por_questao")]

    def __str__(self):
        return f"{self.aluno} — {self.questao}"


class EventoUso(models.Model):
    """Registro de quando o aluno liga um apoio de interface. Alimenta o painel e as sugestões de perfil."""

    class Tipo(models.TextChoices):
        ATIVOU_FONTE_DISLEXIA = "ativou_fonte_dislexia", "Ligou as letras espaçadas"
        ATIVOU_LEITURA_VOZ = "ativou_leitura_voz", "Ligou a leitura em voz alta"
        ATIVOU_MODO_LIMPO = "ativou_modo_limpo", "Ligou o modo limpo"

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="eventos")
    aula = models.ForeignKey(
        Aula, on_delete=models.SET_NULL, null=True, blank=True, related_name="eventos",
        help_text="Aula aberta quando o apoio foi ligado (vazio se foi em outra tela).",
    )
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"{self.aluno} — {self.get_tipo_display()}"


class FeedbackVersao(models.Model):
    """Avaliação do professor sobre uma versão adaptada. Alimenta as métricas de eficácia dos apoios."""

    versao = models.ForeignKey(VersaoAdaptada, on_delete=models.CASCADE, related_name="feedbacks")
    professor = models.ForeignKey(
        "contas.Usuario", on_delete=models.CASCADE, related_name="feedbacks_dados",
        limit_choices_to={"papel": "professor"},
    )
    nota = models.PositiveSmallIntegerField(
        help_text="1 (ruim) a 5 (excelente)",
        choices=[(i, str(i)) for i in range(1, 6)],
    )
    comentario = models.TextField(blank=True, help_text="O que funcionou bem ou mal nesta versão.")
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Nota {self.nota} para {self.versao}"
