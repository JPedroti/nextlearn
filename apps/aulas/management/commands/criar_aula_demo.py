"""
Comando de management: cria dados de demonstração para o hackathon.

Uso:
    python manage.py criar_aula_demo

Cria:
    - Professor demo (prof / senha123)
    - Turma "6º A"
    - Dois alunos: Daniel (perfil textual + leitura em voz alta) e Talita (perfil foco + modo limpo)
    - Uma aula de Equações do 2º grau com 5 questões de múltipla escolha
    - Aula já publicada
"""

from django.core.management.base import BaseCommand

from apps.contas.models import Usuario
from apps.turmas.models import Aluno, Turma
from apps.aulas.models import Aula, Questao
from apps.perfis.models import Perfil


AULA_TITULO = "Equações do 2º grau: fórmula de Bhaskara"

AULA_CONTEUDO = """Uma equação do 2º grau é toda equação que pode ser escrita na forma:

ax² + bx + c = 0

Onde a, b e c são números reais e a ≠ 0. O "a" é o coeficiente do x², o "b" é o coeficiente do x, e o "c" é o termo independente (o número sozinho, sem x).

Para resolver uma equação do 2º grau, usamos a fórmula de Bhaskara:

x = (-b ± √Δ) / (2a)

Onde Δ (delta) é o discriminante:

Δ = b² - 4ac

O valor de delta nos diz quantas soluções a equação tem:
- Se Δ > 0: duas soluções reais diferentes
- Se Δ = 0: uma solução real (as duas raízes são iguais)
- Se Δ < 0: nenhuma solução real (as raízes são números complexos)

Exemplo: resolver x² - 5x + 6 = 0
a = 1, b = -5, c = 6
Δ = (-5)² - 4·1·6 = 25 - 24 = 1
x = (5 ± √1) / 2
x = (5 ± 1) / 2
x₁ = 3, x₂ = 2"""

QUESTOES = [
    {
        "enunciado": "Qual é a fórmula de Bhaskara para resolver ax² + bx + c = 0?",
        "alternativas": [
            "x = -b ± √(b² - 4ac) / 2a",
            "x = b ± √(b² + 4ac) / a",
            "x = -b ± √(b² + 4ac) / 2a",
            "x = b ± √(b² - 4ac) / a",
        ],
        "indice_correto": 0,
    },
    {
        "enunciado": "Na equação 2x² + 3x - 5 = 0, qual é o valor do coeficiente b?",
        "alternativas": [
            "2",
            "3",
            "-5",
            "0",
        ],
        "indice_correto": 1,
    },
    {
        "enunciado": "Calcule o delta (Δ) da equação x² - 6x + 8 = 0.",
        "alternativas": [
            "Δ = -4",
            "Δ = 4",
            "Δ = 36",
            "Δ = 2",
        ],
        "indice_correto": 1,  # b² - 4ac = 36 - 32 = 4
    },
    {
        "enunciado": "Se o delta de uma equação do 2º grau é negativo, o que isso significa?",
        "alternativas": [
            "A equação tem duas soluções reais",
            "A equação tem uma solução real",
            "A equação não tem solução real",
            "A equação tem infinitas soluções",
        ],
        "indice_correto": 2,
    },
    {
        "enunciado": "Resolva a equação x² - 4x + 4 = 0. Qual é a solução?",
        "alternativas": [
            "x = 0",
            "x = 2",
            "x = 4 e x = 0",
            "x = 2 e x = -2",
        ],
        "indice_correto": 1,  # Δ = 0, x = 2 (raiz única)
    },
]


class Command(BaseCommand):
    help = "Cria dados de demonstração: professor, turma, alunos com perfis e uma aula de equações do 2º grau."

    def handle(self, *args, **options):
        # 1. Professor
        professor, created = Usuario.objects.get_or_create(
            username="prof",
            defaults={
                "first_name": "Professor",
                "papel": Usuario.Papel.PROFESSOR,
                "is_staff": True,
            },
        )
        if created:
            professor.set_password("senha123")
            professor.save()
            self.stdout.write(self.style.SUCCESS(f"Professor criado: prof / senha123"))
        else:
            self.stdout.write("Professor 'prof' já existe.")

        # 2. Turma
        turma, created = Turma.objects.get_or_create(
            nome="6º A",
            defaults={"professor": professor},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Turma '{turma.nome}' criada."))
        else:
            self.stdout.write(f"Turma '{turma.nome}' já existe.")

        # 3. Alunos
        alunos_demo = [
            {
                "username": "daniel",
                "first_name": "Daniel",
                "foco": False,
                "textual": True,
                "concreto": False,
                "fonte_dislexia": False,
                "leitura_voz": True,
                "modo_limpo": False,
                "contexto": "O Daniel entende melhor quando o texto é lido em voz alta. "
                            "Prefere frases curtas e diretas, sem figuras de linguagem.",
            },
            {
                "username": "talita",
                "first_name": "Talita",
                "foco": True,
                "textual": False,
                "concreto": False,
                "fonte_dislexia": False,
                "leitura_voz": False,
                "modo_limpo": True,
                "contexto": "A Talita se distrai com facilidade. "
                            "Ela se concentra melhor quando a tela é limpa e o conteúdo vem em passos curtos.",
            },
        ]

        for dados in alunos_demo:
            usuario, created = Usuario.objects.get_or_create(
                username=dados["username"],
                defaults={
                    "first_name": dados["first_name"],
                    "papel": Usuario.Papel.ALUNO,
                },
            )
            if created:
                usuario.set_password("senha123")
                usuario.save()

            aluno, created = Aluno.objects.get_or_create(
                usuario=usuario,
                defaults={"turma": turma},
            )
            if created and aluno.turma != turma:
                aluno.turma = turma
                aluno.save()

            perfil, _ = Perfil.objects.get_or_create(aluno=aluno)
            perfil.foco = dados["foco"]
            perfil.textual = dados["textual"]
            perfil.concreto = dados["concreto"]
            perfil.fonte_dislexia = dados["fonte_dislexia"]
            perfil.leitura_voz = dados["leitura_voz"]
            perfil.modo_limpo = dados["modo_limpo"]
            perfil.contexto_familia = dados["contexto"]
            perfil.revisado_pelo_professor = True
            perfil.save()

            mascara_str = f"{int(perfil.foco)}{int(perfil.textual)}{int(perfil.concreto)}"
            apoios = perfil.nomes_apoios() or ["aula original"]
            self.stdout.write(
                f"  Aluno: {dados['first_name']} (/{dados['username']}) — "
                f"máscara {mascara_str} — {', '.join(apoios)}"
            )

        # 4. Aula
        aula, created = Aula.objects.get_or_create(
            titulo=AULA_TITULO,
            turma=turma,
            defaults={
                "conteudo": AULA_CONTEUDO.strip(),
                "publicada": True,
            },
        )
        if created:
            for i, q in enumerate(QUESTOES, start=1):
                Questao.objects.create(
                    aula=aula,
                    ordem=i,
                    enunciado=q["enunciado"],
                    alternativas=q["alternativas"],
                    indice_correto=q["indice_correto"],
                )
            self.stdout.write(self.style.SUCCESS(
                f"Aula '{AULA_TITULO}' criada com {len(QUESTOES)} questões (já publicada)."
            ))
        else:
            self.stdout.write(f"Aula '{AULA_TITULO}' já existe.")

        self.stdout.write(self.style.SUCCESS("\nDados de demonstração prontos!"))
        self.stdout.write("  Logins: prof/senha123, daniel/senha123, talita/senha123")