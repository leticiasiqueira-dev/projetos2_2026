from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("simulador/", views.simulador)
]


urlpatterns = [
    path("", views.index, name="index"),
    path("simulador/", views.simulador, name="simulador"),
    path("api/maquinas/<int:maquina_id>/telemetria/", views.telemetria_maquina, name="telemetria_maquina"),
]