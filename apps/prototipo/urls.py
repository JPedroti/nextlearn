from django.urls import path

from . import views

app_name = "prototipo"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("aluno/", views.aluno, name="aluno"),
    path("aluno/aula/", views.aula, name="aula"),
    path("professor/", views.professor, name="professor"),
    path("familia/", views.familia, name="familia"),
]
