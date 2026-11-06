from django.test import TestCase
from django.urls import reverse


class EfeitoDominoTests(TestCase):

    def test_pagina_inicial_carrega(self):
        resposta = self.client.get('/efeito_domino/')

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, 'Quando uma máquina para')


# Create your tests here.
