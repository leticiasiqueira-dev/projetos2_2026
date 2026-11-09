
from django.urls import path
from . import views

urlpatterns = [
    path("", views.comparativo, name="comparativo"),
    path("salvar/", views.salvar_simulacao, name="salvar_simulacao"),
]
