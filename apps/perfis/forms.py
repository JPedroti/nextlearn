from django import forms

from .models import PREFERENCIAS, Perfil
from .questionario import OPCOES, PERGUNTAS


class ApoiosForm(forms.ModelForm):
    """O professor marca os apoios de conteúdo (os 3 bits da máscara) e as preferências de tela que já vêm ligadas."""

    class Meta:
        model = Perfil
        fields = ["foco", "textual", "concreto", *PREFERENCIAS]
        widgets = {campo: forms.CheckboxInput(attrs={"class": "mt-1 h-5 w-5"}) for campo in fields}

    def campos_conteudo(self):
        return [self[campo] for campo in ("foco", "textual", "concreto")]

    def campos_interface(self):
        return [self[campo] for campo in PREFERENCIAS]


class QuestionarioForm(forms.Form):
    """Questionário que a família responde: nome do aluno, 9 perguntas (3 por apoio) e um campo aberto."""

    nome_aluno = forms.CharField(
        label="Nome do aluno",
        max_length=120,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm",
                "placeholder": "Como você chama ele(a) em casa?",
            }
        ),
        help_text="Opcional. Pode ser o nome ou o apelido que você usa no dia a dia.",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for pergunta in PERGUNTAS:
            self.fields[pergunta["id"]] = forms.TypedChoiceField(
                label=pergunta["texto"],
                choices=OPCOES,
                coerce=int,
                widget=forms.RadioSelect,
                error_messages={"required": "Por favor, escolha uma resposta para esta pergunta."},
            )

    observacoes = forms.CharField(
        label="Tem mais alguma coisa que você gostaria de compartilhar com o professor?",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "class": "mt-1 block w-full rounded-md border-gray-300 shadow-sm text-sm",
                "placeholder": "Conte um pouco sobre como seu filho(a) aprende melhor. "
                               "O que ajuda? O que atrapalha? O professor vai ler com carinho "
                               "e usar essas informações para adaptar as aulas.",
            }
        ),
        help_text="Opcional. Só o professor lê este texto; ele não é enviado para a inteligência artificial. "
                   "Não é preciso contar diagnóstico nem laudo.",
    )

    def dados_questionario(self):
        """Separa as respostas das perguntas (para o JSONField) dos campos extras (nome e observações)."""
        dados = self.cleaned_data
        respostas = {p["id"]: dados[p["id"]] for p in PERGUNTAS if p["id"] in dados}
        return {
            "respostas": respostas,
            "nome_aluno": dados.get("nome_aluno", ""),
            "observacoes": dados.get("observacoes", ""),
        }