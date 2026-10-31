from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.contas.urls")),
    path("professor/", include("apps.painel.urls")),
    path("familia/", include("apps.perfis.urls")),
    path("aluno/", include("apps.aulas.urls")),
]
