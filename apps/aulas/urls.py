from django.urls import path

from . import views

app_name = "aulas"

urlpatterns = [
    # Professor
    path("professor/turmas/<int:turma_pk>/aulas/nova/", views.nova_aula, name="nova"),
    path("professor/turmas/<int:turma_pk>/aulas/nova-via-pdf/", views.nova_aula_via_pdf, name="nova_via_pdf"),
    path("professor/aulas/<int:pk>/", views.detalhe_professor, name="detalhe_professor"),
    path("professor/aulas/<int:pk>/editar/", views.editar_aula, name="editar"),
    path("professor/aulas/<int:pk>/publicar/", views.alternar_publicacao, name="alternar_publicacao"),
    path("professor/aulas/<int:pk>/versoes/<int:mascara>/gerar/", views.gerar, name="gerar_versao"),
    path("professor/aulas/<int:pk>/versoes/<int:mascara>/", views.revisar_versao, name="revisar_versao"),
    # Aluno
    path("aluno/", views.inicio, name="inicio"),
    path("aluno/aulas/<int:pk>/", views.ver_aula, name="ver"),
]
