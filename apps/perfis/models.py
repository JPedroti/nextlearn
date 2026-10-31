from django.conf import settings
from django.db import models

from apps.turmas.models import Aluno

# Os 3 apoios de conteúdo (bits da máscara), do bit mais alto para o mais baixo.
APOIOS = [
    ("foco", "Atenção e foco", 4),
    ("textual", "Acessibilidade textual", 2),
    ("concreto", "Interativo e concreto", 1),
]


def calcular_mascara(foco, textual, concreto):
    """F*4 + S*2 + C*1 → número de 0 a 7. Zero é a aula original do professor."""
    return int(foco) * 4 + int(textual) * 2 + int(concreto)


def bits_da_mascara(mascara):
    """Caminho inverso: 0–7 → (foco, textual, concreto)."""
    return bool(mascara & 4), bool(mascara & 2), bool(mascara & 1)


def nomes_da_mascara(mascara):
    """Ex.: 5 → ["Atenção e foco", "Interativo e concreto"]."""
    return [nome for _, nome, valor in APOIOS if mascara & valor]


class Perfil(models.Model):
    """Apoios de um aluno. Os 3 bits mudam o conteúdo (IA); as preferências mudam só a interface."""

    aluno = models.OneToOneField(Aluno, on_delete=models.CASCADE, related_name="perfil")

    # Apoios de conteúdo (formam a máscara)
    foco = models.BooleanField(
        "Atenção e foco", default=False, help_text="Aula em passos curtos, um de cada vez, com menos estímulos."
    )
    textual = models.BooleanField(
        "Acessibilidade textual",
        default=False,
        help_text="Linguagem simples e literal, frases curtas, sem figuras de linguagem.",
    )
    concreto = models.BooleanField(
        "Interativo e concreto",
        default=False,
        help_text="Exemplos do dia a dia, analogias e descrição de imagens para ideias abstratas.",
    )

    # Preferências de interface (sem IA): já vêm ligadas para o aluno, que também pode ligar e desligar sozinho
    fonte_dislexia = models.BooleanField(
        "Fonte para dislexia", default=False, help_text="Texto na fonte OpenDyslexic, com mais espaço entre letras."
    )
    leitura_voz = models.BooleanField(
        "Leitura em voz alta", default=False, help_text="Botões para ouvir o texto da aula e as questões."
    )
    modo_limpo = models.BooleanField(
        "Modo limpo", default=False, help_text="Tela com menos cores e enfeites, e letra maior."
    )

    revisado_pelo_professor = models.BooleanField(default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.aluno}"

    @property
    def mascara(self):
        return calcular_mascara(self.foco, self.textual, self.concreto)

    def nomes_apoios(self):
        return nomes_da_mascara(self.mascara)


class RespostaQuestionario(models.Model):
    """Respostas da família sobre o dia a dia do aluno. Sem laudo e sem diagnóstico."""

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="questionarios")
    respostas = models.JSONField(help_text="{id da pergunta: 0 = quase nunca, 1 = às vezes, 2 = com frequência}")
    preenchido_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="questionarios_preenchidos"
    )
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"Questionário de {self.aluno} ({self.criado_em:%d/%m %H:%M})"


class SugestaoPerfil(models.Model):
    """Sugestão de mudar um campo do perfil. Só vale depois que o professor aceita."""

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        ACEITA = "aceita", "Aceita"
        RECUSADA = "recusada", "Recusada"

    class Origem(models.TextChoices):
        QUESTIONARIO = "questionario", "Questionário da família"
        USO = "uso", "Uso da plataforma"

    CAMPOS = [
        ("foco", "Atenção e foco"),
        ("textual", "Acessibilidade textual"),
        ("concreto", "Interativo e concreto"),
        ("fonte_dislexia", "Fonte para dislexia"),
        ("leitura_voz", "Leitura em voz alta"),
        ("modo_limpo", "Modo limpo"),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="sugestoes")
    campo = models.CharField(max_length=20, choices=CAMPOS)
    valor_sugerido = models.BooleanField()
    motivo = models.TextField()
    origem = models.CharField(max_length=20, choices=Origem.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    criada_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criada_em"]

    def __str__(self):
        return f"{self.descricao()} — {self.aluno}"

    def descricao(self):
        acao = "Ligar" if self.valor_sugerido else "Desligar"
        return f"{acao} “{self.get_campo_display()}”"

    def aceitar(self):
        perfil, _ = Perfil.objects.get_or_create(aluno=self.aluno)
        setattr(perfil, self.campo, self.valor_sugerido)
        perfil.revisado_pelo_professor = True
        perfil.save()
        self.status = self.Status.ACEITA
        self.save(update_fields=["status"])

    def recusar(self):
        self.status = self.Status.RECUSADA
        self.save(update_fields=["status"])
