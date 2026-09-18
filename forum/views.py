from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from .models import Pergunta, Resposta


class MainView(View):

    def get(self, request):
        lista_ultimas_questoes = Pergunta.objects.order_by(
            "-data_criacao"
        )

        contexto = {
            "perguntas": lista_ultimas_questoes
        }

        return render(
            request,
            "forum/index.html",
            contexto
        )


class PerguntaView(View):

    def get(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)

        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")

        contexto = {
            "pergunta": pergunta
        }

        return render(
            request,
            "forum/detalhe.html",
            contexto
        )


class VotoView(View):

    def get(self, request, resposta_id):
        try:
            resposta = Resposta.objects.get(pk=resposta_id)

        except Resposta.DoesNotExist:
            raise Http404("Resposta inexistente")

        return HttpResponse(
            str(resposta)
            + "; votos: "
            + str(resposta.votos)
        )

    def post(self, request, resposta_id):
        try:
            resposta = Resposta.objects.get(pk=resposta_id)

        except Resposta.DoesNotExist:
            raise Http404("Resposta inexistente")

        resposta.votos += 1
        resposta.save()

        return redirect(
            reverse(
                "forum:detalhe",
                args=[resposta.pergunta.id]
            )
        )


class InserirPerguntaView(View):

    def get(self, request):
        return render(
            request,
            "forum/inserir_pergunta.html"
        )

    def post(self, request):
        if request.user.is_authenticated:
            usuario = request.user.username
        else:
            usuario = "anônimo"

        titulo = request.POST.get("titulo")
        detalhe = request.POST.get("detalhe")
        tentativa = request.POST.get("tentativa")
        data_criacao = timezone.now()

        pergunta = Pergunta(
            titulo=titulo,
            detalhe=detalhe,
            tentativa=tentativa,
            data_criacao=data_criacao,
            usuario=usuario
        )

        pergunta.save()

        return redirect(
            reverse(
                "forum:detalhe",
                args=[pergunta.id]
            )
        )


class InserirRespostaView(View):

    def get(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)

        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")

        contexto = {
            "pergunta": pergunta
        }

        return render(
            request,
            "forum/inserir_resposta.html",
            contexto
        )

    def post(self, request, pergunta_id):
        try:
            pergunta = Pergunta.objects.get(pk=pergunta_id)

        except Pergunta.DoesNotExist:
            raise Http404("Pergunta inexistente")

        if request.user.is_authenticated:
            usuario = request.user.username
        else:
            usuario = "anônimo"

        texto = request.POST.get("texto_resposta")
        data_criacao = timezone.now()

        pergunta.resposta_set.create(
            texto=texto,
            data_criacao=data_criacao,
            usuario=usuario
        )

        return redirect(
            reverse(
                "forum:detalhe",
                args=[pergunta.id]
            )
        )
