from django.contrib import admin

from .models import Aula, Questao, Resposta, VersaoAdaptada


class QuestaoInline(admin.StackedInline):
    model = Questao
    extra = 0


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "turma", "publicada", "criada_em")
    list_filter = ("turma", "publicada")
    inlines = [QuestaoInline]


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ("aluno", "questao", "indice_escolhido", "correta", "criado_em")
    list_filter = ("correta", "questao__aula")


@admin.register(VersaoAdaptada)
class VersaoAdaptadaAdmin(admin.ModelAdmin):
    list_display = ("aula", "mascara", "aprovada", "gerada_em")
    list_filter = ("aprovada", "mascara")
