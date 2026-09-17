from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("""
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

        <a href="/simulador/">
            Explorar simulador
        </a>
    """)