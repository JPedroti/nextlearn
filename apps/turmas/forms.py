from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.contas.models import Usuario

from .models import Turma


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = ["nome"]
        labels = {"nome": "Nome da turma"}


class NovoAlunoForm(UserCreationForm):
    """O professor cria o login do aluno: nome, usuário e senha inicial."""

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("first_name", "last_name", "username")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True


class NovaFamiliaForm(UserCreationForm):
    """O professor cria o login da família (responsável) do aluno."""

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("first_name", "last_name", "username")
        labels = {"first_name": "Nome do responsável", "last_name": "Sobrenome"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].required = True
