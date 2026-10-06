from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import RedirectView


urlpatterns = [
    # Interface administrativa
    path(
        "admin/",
        admin.site.urls
    ),

    # Projeto sobre IoT
    path(
        "efeito_domino/",
        include("efeito_domino.urls")
    ),

    # Aplicativo do fórum
    path(
        "forum/",
        include("forum.urls")
    ),

    path(
        "quem_somos/", 
        include("quem_somos.urls")),

    # Ao acessar a raiz, redireciona para o fórum
    path(
        "",
        RedirectView.as_view(
            url="/forum/",
            permanent=False
        ),
        name="home"
    ),
]