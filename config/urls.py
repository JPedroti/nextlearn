from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.contas.urls")),
    path("professor/", include("apps.painel.urls")),
    path("professor/turmas/", include("apps.turmas.urls")),
    path("familia/", include("apps.perfis.urls")),
    path("", include("apps.aulas.urls")),  # rotas do professor (/professor/aulas/...) e do aluno (/aluno/...)
]
