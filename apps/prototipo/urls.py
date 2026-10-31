from django.urls import path

from . import views

app_name = "prototipo"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("entrar/", views.entrada, name="entrada"),
    path("login/", views.Login.as_view(), name="login"),
    path("_versao/", views.versao, name="versao"),
    path("aluno/inicio/", views.painel_aluno, name="painel_aluno"),
    path("aluno/fala/", views.fala, name="fala"),
    path("aluno/aula/<int:pk>/online/", views.aula_online, name="aula_online"),
    path("aluno/aula/<int:pk>/online/evento/", views.aula_online_evento, name="aula_online_evento"),
    path("professor/aulas/", views.prof_aulas, name="prof_aulas"),
    path("professor/material/", views.prof_material, name="prof_material"),
    path("professor/material/publicar/", views.prof_publicar, name="prof_publicar"),
    path("professor/aulas/<int:pk>/analise/", views.prof_analise, name="prof_analise"),
    path("como-resolvemos/", views.como_resolvemos, name="como_resolvemos"),
    path("aluno/chat/", views.chat, name="chat"),
    path("aluno/progresso/", views.progresso, name="progresso"),
    path("dev/comparar/", views.comparar, name="comparar"),
    path("aluno/treino/<str:tipo>/", views.treino, name="treino"),
    path("aluno/treino/<str:tipo>/concluido/", views.treino_concluido, name="treino_concluido"),
    path("aluno/", views.aluno, name="aluno"),
    path("aluno/aula/", views.aula, name="aula"),
    path("professor/", views.professor, name="professor"),
    path("professor/alunos/cadastrar/", views.prof_cadastrar, name="prof_cadastrar"),
    path("professor/alunos/<int:pk>/", views.prof_aluno, name="prof_aluno"),
    path("professor/recados/<int:pk>/lido/", views.prof_recado_lido, name="prof_recado_lido"),
    path("familia/", views.familia, name="familia"),
]
