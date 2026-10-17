import json
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8" />
            <title>Efeito Dominó — BZU</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <style>
                :root {
                    --bg: #14081f; --panel: #1f1033; --line: #3a2158;
                    --text: #f4eefb; --muted: #a996c4; --magenta: #d946c7;
                }
                body {
                    margin: 0;
                    min-height: 100vh;
                    background: radial-gradient(120% 140% at 15% 0%, #24123f 0%, var(--bg) 55%);
                    color: var(--text);
                    font-family: -apple-system, "Segoe UI", Inter, system-ui, sans-serif;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 24px;
                    box-sizing: border-box;
                }
                .card {
                    max-width: 700px;
                    background: var(--panel);
                    border: 1px solid var(--line);
                    border-radius: 22px;
                    padding: 40px;
                }
                h1 { font-size: 26px; margin: 0 0 16px; letter-spacing: -0.01em; }
                h2 { font-size: 18px; color: var(--magenta); margin: 28px 0 12px; }
                p { color: var(--muted); line-height: 1.6; font-size: 15px; }
                a.botao {
                    display: inline-block;
                    margin-top: 24px;
                    background: linear-gradient(135deg, #b6349d, #7c3aed);
                    color: var(--text);
                    text-decoration: none;
                    font-weight: 600;
                    padding: 12px 22px;
                    border-radius: 10px;
                    font-size: 14px;
                }
                a.botao:hover { opacity: 0.9; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>Quando uma máquina para, o problema pode não parar nela.</h1>

                <p>
                    Uma pequena falha pode desencadear uma sequência de
                    consequências em uma operação industrial.
                </p>

                <h2>Máquina → Produção → Pedido → Cliente → Prejuízo</h2>

                <p>
                    Descubra como a tecnologia IoT pode ajudar a interromper
                    esse efeito dominó.
                </p>

                <a class="botao" href="/efeito_domino/simulador/">
                    Explorar simulador
                </a>
            </div>
        </body>
        </html>
    """)

import os
from django.conf import settings
from django.http import HttpResponse
from forum.models import Pergunta

def simulador(request):
    ocorrencia = Pergunta.objects.order_by("-data_criacao").first()
 
    if ocorrencia:
        dados_ocorrencia = {
            "titulo": ocorrencia.titulo,
            "detalhe": ocorrencia.detalhe,
        }
    else:
        dados_ocorrencia = None
 
    caminho = os.path.join(
        settings.BASE_DIR, "efeito_domino", "templates", "efeito_domino", "simulador.html"
    )
    with open(caminho, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()
 
    script_dados = "<script>window.OCORRENCIA = " + json.dumps(dados_ocorrencia) + ";</script>"
    conteudo = conteudo.replace("<!--OCORRENCIA_REAL-->", script_dados)
 
    return HttpResponse(conteudo)



import random
from django.http import JsonResponse, Http404

MAQUINAS = {
    1: {"nome": "Máquina 01 — Recepção",       "temp": 58, "vib": 2.0, "efi": 94},
    2: {"nome": "Máquina 02 — Processamento",  "temp": 74, "vib": 3.8, "efi": 88},
    3: {"nome": "Máquina 03 — Montagem",       "temp": 64, "vib": 2.8, "efi": 92},
    4: {"nome": "Máquina 04 — Expedição",      "temp": 55, "vib": 1.8, "efi": 95},
}

LIMITE_TEMP = 80      # °C (máximo)
LIMITE_VIB = 5.0      # mm/s (máximo)
LIMITE_EFI = 85       # % (mínimo)


def telemetria_maquina(request, maquina_id):
    base = MAQUINAS.get(maquina_id)
    if base is None:
        raise Http404("Máquina não encontrada")

    temp = round(base["temp"] + random.uniform(-3, 8), 1)
    vib = round(base["vib"] + random.uniform(-0.6, 2.0), 2)
    efi = round(base["efi"] + random.uniform(-6, 4), 1)
    uptime = round(random.uniform(98.5, 99.9), 1)

    return JsonResponse({
        "nome": base["nome"],
        "temperatura": {"valor": temp, "unidade": "°C", "escala": 100,
                        "acima": temp > LIMITE_TEMP, "regra": f"máx. {LIMITE_TEMP} °C"},
        "vibracao": {"valor": vib, "unidade": "mm/s", "escala": 8,
                     "acima": vib > LIMITE_VIB, "regra": f"máx. {LIMITE_VIB} mm/s"},
        "eficiencia": {"valor": efi, "unidade": "%", "escala": 100,
                       "acima": efi < LIMITE_EFI, "regra": f"mín. {LIMITE_EFI}%"},
        "uptime": {"valor": uptime, "unidade": "%", "escala": 100,
                   "acima": False, "regra": "meta 99%"},
    })