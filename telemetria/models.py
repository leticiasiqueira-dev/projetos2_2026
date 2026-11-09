import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone

LIMITE_OFFLINE_SEGUNDOS = 180  # 3 minutos sem leitura = Offline


def gerar_token():
    return secrets.token_urlsafe(32)


def segundos_desde(momento):
    if momento is None:
        return None
    return max(0, int((timezone.now() - momento).total_seconds()))


def esta_online(segundos):
    return segundos is not None and segundos <= LIMITE_OFFLINE_SEGUNDOS


class Dispositivo(models.Model):
    nome = models.CharField(max_length=100)
    intervalo_envio = models.PositiveIntegerField(default=30, help_text="Segundos entre leituras")
    token = models.CharField(max_length=64, unique=True, default=gerar_token, editable=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Leitura(models.Model):
    dispositivo = models.ForeignKey(Dispositivo, on_delete=models.CASCADE, related_name="leituras")
    temperatura = models.FloatField()
    registrado_em = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [models.Index(fields=["dispositivo", "-id"])]

    def __str__(self):
        return f"{self.dispositivo} · {self.temperatura} °C"