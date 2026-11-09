import json
import math
import secrets

from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import LIMITE_OFFLINE_SEGUNDOS, Dispositivo, Leitura, esta_online, segundos_desde


def _itens_status():
    dispositivos = Dispositivo.objects.annotate(ultima=Max("leituras__registrado_em")).order_by("nome")
    itens = []
    for d in dispositivos:
        segundos = segundos_desde(d.ultima)
        itens.append({"id": d.id, "nome": d.nome, "online": esta_online(segundos), "segundos": segundos})
    return itens


def lista(request):
    return render(request, "telemetria/lista.html", {"itens": _itens_status()})


@require_GET
def api_status(request):
    return JsonResponse({"dispositivos": _itens_status()})


def painel(request, dispositivo_id):
    dispositivo = Dispositivo.objects.filter(pk=dispositivo_id).first()
    if dispositivo is None:
        # Cenário 3: mensagem e nenhum gráfico
        return render(
            request,
            "telemetria/painel.html",
            {"dispositivo": None, "dispositivo_id": dispositivo_id},
            status=404,
        )
    return render(
        request,
        "telemetria/painel.html",
        {"dispositivo": dispositivo, "limite_offline": LIMITE_OFFLINE_SEGUNDOS},
    )


@require_GET
def api_dados(request, dispositivo_id):
    dispositivo = Dispositivo.objects.filter(pk=dispositivo_id).first()
    if dispositivo is None:
        return JsonResponse({"erro": "Dispositivo não encontrado"}, status=404)

    leituras_qs = dispositivo.leituras.all()
    apos = request.GET.get("apos", "")
    if apos.isdigit():
        leituras = list(leituras_qs.filter(id__gt=int(apos)).order_by("id")[:200])
    else:
        leituras = list(leituras_qs.order_by("-id")[:30])[::-1]

    ultima = leituras_qs.aggregate(m=Max("registrado_em"))["m"]
    segundos = segundos_desde(ultima)

    return JsonResponse({
        "leituras": [
            {"id": l.id, "temperatura": l.temperatura, "registrado_em": l.registrado_em.isoformat()}
            for l in leituras
        ],
        "segundos_desde_ultima": segundos,
        "online": esta_online(segundos),
    })


@csrf_exempt
@require_POST
def receber_leitura(request, dispositivo_id):
    dispositivo = Dispositivo.objects.filter(pk=dispositivo_id).first()
    if dispositivo is None:
        return JsonResponse({"erro": "Dispositivo não encontrado"}, status=404)

    chave = request.headers.get("X-API-Key", "")
    if not secrets.compare_digest(chave.encode(), dispositivo.token.encode()):
        return JsonResponse({"erro": "Chave inválida"}, status=401)

    try:
        temperatura = float(json.loads(request.body)["temperatura"])
        if not math.isfinite(temperatura):
            raise ValueError
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"erro": "Envie JSON com o campo numérico 'temperatura'"}, status=400)

    Leitura.objects.create(dispositivo=dispositivo, temperatura=temperatura)
    return JsonResponse({"ok": True}, status=201)