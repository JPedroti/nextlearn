from django import forms

from .models import Perfil


class ApoiosForm(forms.ModelForm):
    """O professor marca os apoios de conteúdo do aluno (os 3 bits da máscara)."""

    class Meta:
        model = Perfil
        fields = ["foco", "textual", "concreto"]
        widgets = {campo: forms.CheckboxInput(attrs={"class": "mt-1 h-5 w-5"}) for campo in fields}
