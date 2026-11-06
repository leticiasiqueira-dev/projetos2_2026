from django.test import TestCase
from django.urls import reverse


class EfeitoDominoTests(TestCase):

    def test_pagina_inicial_carrega(self):
        resposta = self.client.get('/efeito_domino/')

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Quando uma máquina para')


    def test_simulador_carrega(self):
        resposta = self.client.get('/efeito_domino/simulador/')

        self.assertEqual(resposta.status_code, 200)
    
    def test_telemetria_maquina_retorna_dados(self):
        resposta = self.client.get(
            '/efeito_domino/api/maquinas/1/telemetria/'
        )

        self.assertEqual(resposta.status_code, 200)

        dados = resposta.json()

        self.assertIn('temperatura', dados)
        self.assertIn('vibracao', dados)
        self.assertIn('eficiencia', dados)




# Create your tests here.
