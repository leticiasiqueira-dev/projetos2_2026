from django.contrib import admin

from .models import Dispositivo, Leitura


@admin.register(Dispositivo)
class DispositivoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "intervalo_envio", "criado_em")
    readonly_fields = ("token", "criado_em")


@admin.register(Leitura)
class LeituraAdmin(admin.ModelAdmin):
    list_display = ("dispositivo", "temperatura", "registrado_em")
    list_filter = ("dispositivo",)