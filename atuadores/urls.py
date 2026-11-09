
from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel, name='painel_atuadores'),
    path('<int:atuador_id>/comando/', views.enviar_comando, name='enviar_comando'),
]
