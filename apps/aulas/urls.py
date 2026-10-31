from django.urls import path

from . import views

app_name = "aulas"

urlpatterns = [
    # Professor
    path("professor/turmas/<int:turma_pk>/aulas/nova/", views.nova_aula, name="nova"),
    path("professor/aulas/<int:pk>/", views.detalhe_professor, name="detalhe_professor"),
    path("professor/aulas/<int:pk>/editar/", views.editar_aula, name="editar"),
    path("professor/aulas/<int:pk>/publicar/", views.alternar_publicacao, name="alternar_publicacao"),
    # Aluno
    path("aluno/", views.inicio, name="inicio"),
    path("aluno/aulas/<int:pk>/", views.ver_aula, name="ver"),
]
