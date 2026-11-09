from django.urls import path

from . import views

app_name = "telemetria"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("status/", views.api_status, name="status"),
    path("<int:dispositivo_id>/telemetria", views.painel, name="painel"),
    path("<int:dispositivo_id>/telemetria/", views.painel),
    path("<int:dispositivo_id>/dados/", views.api_dados, name="dados"),
    path("<int:dispositivo_id>/leituras/", views.receber_leitura, name="receber"),
]