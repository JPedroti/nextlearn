from django.contrib import admin

from .models import Perfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("aluno", "foco", "textual", "concreto", "mascara", "revisado_pelo_professor")
    list_filter = ("aluno__turma",)
