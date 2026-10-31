from django.contrib import admin

from .models import Perfil, RespostaQuestionario, SugestaoPerfil


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("aluno", "foco", "textual", "concreto", "mascara", "revisado_pelo_professor")
    list_filter = ("aluno__turma",)


@admin.register(RespostaQuestionario)
class RespostaQuestionarioAdmin(admin.ModelAdmin):
    list_display = ("aluno", "preenchido_por", "criado_em")


@admin.register(SugestaoPerfil)
class SugestaoPerfilAdmin(admin.ModelAdmin):
    list_display = ("aluno", "campo", "valor_sugerido", "origem", "status", "criada_em")
    list_filter = ("status", "origem")
