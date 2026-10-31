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

    # Preferências de interface (sem IA; usadas a partir da Fatia 3)
    fonte_dislexia = models.BooleanField(default=False)
    leitura_voz = models.BooleanField(default=False)
    modo_limpo = models.BooleanField(default=False)

    revisado_pelo_professor = models.BooleanField(default=False)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.aluno}"

    @property
    def mascara(self):
        return calcular_mascara(self.foco, self.textual, self.concreto)

    def nomes_apoios(self):
        return nomes_da_mascara(self.mascara)
