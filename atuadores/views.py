
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, permission_required

from .models import Atuador


@login_required
def painel(request):
    atuadores = Atuador.objects.filter(ativo=True)

    return render(request, 'atuadores/painel.html', {
        'atuadores': atuadores
    })


@login_required
@permission_required('atuadores.enviar_comando_atuador', raise_exception=True)
@require_POST
def enviar_comando(request, atuador_id):
    atuador = get_object_or_404(Atuador, id=atuador_id, ativo=True)

    comando = request.POST.get('comando')

    if comando not in ['LIGAR', 'DESLIGAR']:
        return JsonResponse({
            'sucesso': False,
            'mensagem': 'Comando inválido.'
        }, status=400)

    return JsonResponse({
        'sucesso': True,
        'mensagem': 'Comando recebido e aguardando integração MQTT.',
        'atuador': atuador.nome,
        'comando': comando
    })
