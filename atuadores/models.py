from django.db import models

# Create your models here.

class Atuador(models.Model):

    TIPOS = [
        ('VALVULA', 'Válvula'),
        ('EXAUSTOR', 'Exaustor'),
        ('MOTOR', 'Motor'),
        ('OUTRO', 'Outro'),
    ]

    nome = models.CharField(max_length=100)

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS
    )

    topico_mqtt = models.CharField(max_length=200, unique=True)

    estado = models.BooleanField(default=False)

    ativo = models.BooleanField(default=True)

    ultima_atualizacao = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        permissions = [
            ('enviar_comando_atuador', 'Pode enviar comandos aos atuadores'),
        ]

    def __str__(self):
        return self.nome
