from django.contrib import admin

from .models import Aluno, Turma


@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ("nome", "professor", "criada_em")


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "turma", "responsavel")
    list_filter = ("turma",)
