"""
Testes E2E (Selenium) - app telemetria
  US07 - Visualização de telemetria em tempo real (dashboard)

O painel consulta a API a cada 5 s, então os testes de "tempo real"
esperam até 20 s (WebDriverWait) sem recarregar a página.
"""
from datetime import timedelta

from django.utils import timezone
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from project.selenium_base import BaseTestCase
from telemetria.models import Dispositivo, Leitura

JS_PONTOS_NO_GRAFICO = (
    "return Chart.getChart(document.getElementById('grafico'))"
    ".data.datasets[0].data.length;"
)


class Teste_07_US07_DashboardTelemetria(BaseTestCase):
    """US07: gráficos de telemetria atualizados em tempo real."""

    def criar_dispositivo(self, nome="Sensor da Linha 1", temperaturas=(), minutos_atras=0):
        dispositivo = Dispositivo.objects.create(nome=nome)
        agora = timezone.now() - timedelta(minutes=minutos_atras)
        for t in temperaturas:
            Leitura.objects.create(
                dispositivo=dispositivo, temperatura=t, registrado_em=agora
            )
        return dispositivo

    def url_painel(self, dispositivo):
        return f"/forum/dispositivos/{dispositivo.id}/telemetria/"

    def test_01_deve_exibir_painel_com_leituras_e_grafico(self):
        print("US07 - Teste 01: Painel com temperatura atual e gráfico.")

        disp = self.criar_dispositivo(temperaturas=[21.0, 22.5, 23.4])
        self.abrir_pagina(self.url_painel(disp))

        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "temp-atual"), "23.4")
        )
        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "status"), "Online")
        )
        self.assertTrue(self.driver.find_element(By.ID, "grafico").is_displayed())
        self.assertEqual(self.driver.execute_script(JS_PONTOS_NO_GRAFICO), 3)
        self.assertFalse(
            self.driver.find_element(By.ID, "alerta-offline").is_displayed()
        )

        self.pausa(3)

    def test_02_deve_atualizar_grafico_sem_recarregar_a_pagina(self):
        print("US07 - Teste 02: Nova leitura aparece sem recarregar.")

        disp = self.criar_dispositivo(temperaturas=[20.0])
        self.abrir_pagina(self.url_painel(disp))
        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "temp-atual"), "20.0")
        )

        # marcador na página: se ela recarregar, o marcador desaparece
        self.driver.execute_script("window.marcadorSemRecarga = 'ok';")

        # chega uma nova leitura do sensor
        Leitura.objects.create(dispositivo=disp, temperatura=30.5)

        WebDriverWait(self.driver, 20).until(
            EC.text_to_be_present_in_element((By.ID, "temp-atual"), "30.5")
        )
        self.assertEqual(
            self.driver.execute_script("return window.marcadorSemRecarga;"), "ok"
        )
        self.assertEqual(self.driver.execute_script(JS_PONTOS_NO_GRAFICO), 2)

        self.pausa(3)

    def test_03_deve_indicar_offline_quando_nao_ha_leituras(self):
        print("US07 - Teste 03: Dispositivo sem leituras aparece Offline.")

        disp = self.criar_dispositivo(nome="Sensor Sem Sinal")
        self.abrir_pagina(self.url_painel(disp))

        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "status"), "Offline")
        )
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "alerta-offline"))
        )
        self.assertEqual(self.driver.find_element(By.ID, "temp-atual").text, "—")

        self.pausa(2)

    def test_04_deve_indicar_offline_quando_leitura_e_antiga(self):
        print("US07 - Teste 04: Última leitura há 10 min => Offline.")

        disp = self.criar_dispositivo(temperaturas=[25.0], minutos_atras=10)
        self.abrir_pagina(self.url_painel(disp))

        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "temp-atual"), "25.0")
        )
        self.wait.until(
            EC.text_to_be_present_in_element((By.ID, "status"), "Offline")
        )
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "alerta-offline"))
        )

        self.pausa(2)

    def test_05_deve_exibir_mensagem_para_dispositivo_inexistente(self):
        print("US07 - Teste 05: Dispositivo inexistente não mostra gráfico.")

        self.abrir_pagina("/forum/dispositivos/9999/telemetria/")

        h1 = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        self.assertIn("Dispositivo não encontrado", h1.text)
        self.assertEqual(self.driver.find_elements(By.ID, "grafico"), [])

        self.pausa(2)

    def test_06_deve_abrir_painel_a_partir_da_lista_de_dispositivos(self):
        print("US07 - Teste 06: Lista de dispositivos -> painel.")

        self.criar_dispositivo(nome="Sensor da Caldeira", temperaturas=[40.0])
        self.abrir_pagina("/forum/dispositivos/")

        self.wait.until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Sensor da Caldeira"))
        ).click()

        self.wait.until(EC.url_contains("/telemetria"))
        self.wait.until(EC.visibility_of_element_located((By.ID, "grafico")))

        self.pausa(3)