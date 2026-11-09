
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST


# US09 - Exibir comparativo das simulações
def comparativo(request):
    simulacao1 = request.session.get("simulacao1")
    simulacao2 = request.session.get("simulacao2")

    if not simulacao1 or not simulacao2:
        return render(request, "comparativo/resultado.html", {
            "erro": "É necessário concluir as duas simulações."
        })

    return render(request, "comparativo/resultado.html", {
        "simulacao1": simulacao1,
        "simulacao2": simulacao2
    })


# US09 - Salvar os resultados das simulações
@require_POST
def salvar_simulacao(request):
    try:
        dados = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({
            "erro": "Dados inválidos"
        }, status=400)

    tipo = dados.get("tipo")

    if tipo not in ["simulacao1", "simulacao2"]:
        return JsonResponse({
            "erro": "Tipo inválido"
        }, status=400)

    request.session[tipo] = {
        "tempo": dados.get("tempo")
    }

    return JsonResponse({
        "sucesso": True
    })
