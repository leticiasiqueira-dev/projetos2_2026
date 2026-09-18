from django.urls import path

from . import views


app_name = "forum"

urlpatterns = [
    # Página inicial do fórum: /forum/
    path(
        "",
        views.MainView.as_view(),
        name="index"
    ),

    # Detalhes de uma pergunta: /forum/1/
    path(
        "<int:pergunta_id>/",
        views.PerguntaView.as_view(),
        name="detalhe"
    ),

    # Votar em uma resposta: /forum/1/voto/
    path(
        "<int:resposta_id>/voto/",
        views.VotoView.as_view(),
        name="voto"
    ),

    # Criar pergunta: /forum/inserir/
    path(
        "inserir/",
        views.InserirPerguntaView.as_view(),
        name="inserir_pergunta"
    ),

    # Criar resposta: /forum/1/resposta/
    path(
        "<int:pergunta_id>/resposta/",
        views.InserirRespostaView.as_view(),
        name="inserir_resposta"
    ),
]