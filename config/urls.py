from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("jogo/", include("apps.prototipo.urls")),  # Protótipo de gamificação
    path("", include("apps.contas.urls")),
    path("professor/", include("apps.painel.urls")),
    path("professor/turmas/", include("apps.turmas.urls")),
    # Os apps abaixo têm rotas do professor (/professor/...) e da família ou do aluno.
    path("", include("apps.perfis.urls")),
    path("", include("apps.aulas.urls")),
]
