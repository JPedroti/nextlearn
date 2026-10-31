from django.urls import path

from . import views

app_name = "perfis"

urlpatterns = [
    # Família
    path("familia/", views.inicio, name="inicio"),
    # Professor
    path("professor/alunos/<int:aluno_pk>/apoios/", views.editar_apoios, name="editar_apoios"),
]
