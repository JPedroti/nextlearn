from django.urls import path

from . import views

app_name = "painel"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("turmas/<int:pk>/painel/", views.turma, name="turma"),
]
