from django import forms

from .models import Aula, Questao

LETRAS = "ABCD"


class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ["titulo", "conteudo"]
        labels = {"titulo": "Título", "conteudo": "Texto da aula"}
        help_texts = {"conteudo": "Escreva como você daria a aula. Esta é a versão original, a base de todas as adaptações."}
        widgets = {"conteudo": forms.Textarea(attrs={"rows": 12})}


class QuestaoForm(forms.ModelForm):
    """Uma questão com até 4 alternativas (A–D). Pelo menos 2 precisam estar preenchidas."""

    alternativa_a = forms.CharField(label="A", required=False, max_length=500)
    alternativa_b = forms.CharField(label="B", required=False, max_length=500)
    alternativa_c = forms.CharField(label="C", required=False, max_length=500)
    alternativa_d = forms.CharField(label="D", required=False, max_length=500)
    correta = forms.ChoiceField(
        label="Alternativa correta",
        choices=[(letra, letra) for letra in LETRAS],
        widget=forms.RadioSelect,
        required=False,
    )

    class Meta:
        model = Questao
        fields = ["enunciado"]
        widgets = {"enunciado": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ao editar, preenche os campos A–D com as alternativas já salvas.
        if self.instance.pk:
            for letra, texto in zip(LETRAS, self.instance.alternativas):
                self.initial[f"alternativa_{letra.lower()}"] = texto
            self.initial["correta"] = LETRAS[self.instance.indice_correto]

    def campos_alternativas(self):
        return [self[f"alternativa_{letra.lower()}"] for letra in LETRAS]

    def clean(self):
        dados = super().clean()
        preenchidas = [
            (letra, dados.get(f"alternativa_{letra.lower()}", "").strip())
            for letra in LETRAS
            if dados.get(f"alternativa_{letra.lower()}", "").strip()
        ]
        if len(preenchidas) < 2:
            raise forms.ValidationError("Preencha pelo menos 2 alternativas.")
        letras_preenchidas = [letra for letra, _ in preenchidas]
        correta = dados.get("correta")
        if not correta:
            raise forms.ValidationError("Marque qual alternativa é a correta.")
        if correta not in letras_preenchidas:
            raise forms.ValidationError("A alternativa marcada como correta está vazia.")
        dados["alternativas_lista"] = [texto for _, texto in preenchidas]
        dados["indice_correto"] = letras_preenchidas.index(correta)
        return dados

    def save(self, commit=True):
        self.instance.alternativas = self.cleaned_data["alternativas_lista"]
        self.instance.indice_correto = self.cleaned_data["indice_correto"]
        return super().save(commit)


QuestaoFormSet = forms.inlineformset_factory(
    Aula,
    Questao,
    form=QuestaoForm,
    extra=4,
    min_num=1,
    validate_min=True,
    can_delete=True,
)


class VersaoForm(forms.Form):
    """O professor revisa (e pode corrigir) o texto e os enunciados gerados pela IA antes de aprovar."""

    conteudo = forms.CharField(label="Texto da aula adaptado", widget=forms.Textarea(attrs={"rows": 14}))

    def __init__(self, *args, versao, questoes, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["conteudo"].initial = versao.conteudo
        self.questoes = questoes
        for i, (questao, enunciado) in enumerate(zip(questoes, versao.enunciados)):
            self.fields[f"enunciado_{i}"] = forms.CharField(
                label=f"Enunciado da questão {questao.ordem}",
                initial=enunciado,
                widget=forms.Textarea(attrs={"rows": 3}),
            )

    def itens(self):
        """Pares (campo do enunciado, questão) para mostrar as alternativas do professor ao lado."""
        return [(self[f"enunciado_{i}"], questao) for i, questao in enumerate(self.questoes)]

    def enunciados(self):
        return [self.cleaned_data[f"enunciado_{i}"].strip() for i in range(len(self.questoes))]
