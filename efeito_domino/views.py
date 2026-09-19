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