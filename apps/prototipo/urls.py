from django.urls import path

from . import views

app_name = "prototipo"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("entrar/", views.entrada, name="entrada"),
    path("login/", views.Login.as_view(), name="login"),
    path("_versao/", views.versao, name="versao"),
    path("aluno/inicio/", views.painel_aluno, name="painel_aluno"),
    path("aluno/treino/<str:tipo>/", views.treino, name="treino"),
    path("aluno/", views.aluno, name="aluno"),
    path("aluno/aula/", views.aula, name="aula"),
    path("professor/", views.professor, name="professor"),
    path("familia/", views.familia, name="familia"),
]
