from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("""
        <h1>Quem Somos</h1>
        <p>
            Somos uma equipe de estudantes dedicada ao desenvolvimento de
            soluções tecnológicas para a BZU, utilizando inovação e tecnologia
            para transformar dados em informações úteis para a tomada de decisões.
        </p>""")