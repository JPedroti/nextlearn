from django.urls import path

from . import views

app_name = "perfis"

urlpatterns = [
    # Aluno
    path("aluno/preferencias/", views.alternar_preferencia, name="alternar_preferencia"),
    # Família
    path("familia/", views.inicio, name="inicio"),
    path("familia/alunos/<int:aluno_pk>/questionario/", views.questionario, name="questionario"),
    path("familia/alunos/<int:aluno_pk>/relatorio/", views.relatorio, name="relatorio"),
    # Professor
    path("professor/alunos/<int:aluno_pk>/apoios/", views.editar_apoios, name="editar_apoios"),
    path("professor/alunos/<int:aluno_pk>/dashboard/", views.dashboard, name="dashboard"),
    path("professor/sugestoes/<int:pk>/aceitar/", views.responder_sugestao, {"aceitar": True}, name="aceitar_sugestao"),
    path("professor/sugestoes/<int:pk>/recusar/", views.responder_sugestao, {"aceitar": False}, name="recusar_sugestao"),
]
