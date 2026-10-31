from django.urls import path

from . import views

app_name = "turmas"

urlpatterns = [
    path("nova/", views.nova_turma, name="nova"),
    path("<int:pk>/", views.detalhe, name="detalhe"),
    path("<int:pk>/alunos/novo/", views.novo_aluno, name="novo_aluno"),
]
