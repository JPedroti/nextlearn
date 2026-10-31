from django import forms

from .models import Perfil
from .questionario import OPCOES, PERGUNTAS


class ApoiosForm(forms.ModelForm):
    """O professor marca os apoios de conteúdo do aluno (os 3 bits da máscara)."""

    class Meta:
        model = Perfil
        fields = ["foco", "textual", "concreto"]
        widgets = {campo: forms.CheckboxInput(attrs={"class": "mt-1 h-5 w-5"}) for campo in fields}


class QuestionarioForm(forms.Form):
    """Uma pergunta de múltipla escolha (quase nunca / às vezes / com frequência) para cada item do questionário."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for pergunta in PERGUNTAS:
            self.fields[pergunta["id"]] = forms.TypedChoiceField(
                label=pergunta["texto"],
                choices=OPCOES,
                coerce=int,
                widget=forms.RadioSelect,
                error_messages={"required": "Escolha uma resposta."},
            )
