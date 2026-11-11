from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from project.selenium_base import BaseTestCase

BOTAO_COMPARATIVO = "Ver comparativo das simulações"
SELETOR_SALVAS = ".us9-status span.sucesso"


class Teste_09_US09_Comparativo(BaseTestCase):
    """US09: comparativo entre os cenários com e sem monitoramento IoT."""

    def esperar_simulacoes_salvas(self, quantidade):
        self.wait_longo.until(
            lambda d: len(d.find_elements(By.CSS_SELECTOR, SELETOR_SALVAS)) >= quantidade
        )

    def test_01_deve_informar_que_comparativo_esta_indisponivel_sem_simulacoes(self):
        print("US09 - Teste 01: Comparativo sem nenhuma simulação.")

        self.abrir_pagina("/comparativo/")

        body = self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        ).text
        self.assertIn("Comparativo indisponível", body)
        self.assertIn("É necessário concluir as duas simulações.", body)

        self.pausa(2)

    def test_02_nao_deve_liberar_comparativo_com_apenas_uma_simulacao(self):
        print("US09 - Teste 02: Apenas a simulação sem BZU concluída.")

        self.abrir_simulador()

        # botão do comparativo começa desabilitado
        botao = self.driver.find_element(
            By.XPATH, f"//button[normalize-space(.)='{BOTAO_COMPARATIVO}']"
        )
        self.assertFalse(botao.is_enabled())

        self.clicar_botao("Simular sem BZU")
        self.esperar_simulacoes_salvas(1)

        # continua desabilitado: falta a simulação com BZU
        self.assertFalse(botao.is_enabled())

        # abrir a URL direto também mostra o aviso
        self.abrir_pagina("/comparativo/")
        body = self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        ).text
        self.assertIn("É necessário concluir as duas simulações.", body)

        self.pausa(3)

    def test_03_deve_exibir_comparativo_apos_as_duas_simulacoes(self):
        print("US09 - Teste 03: Fluxo completo até o comparativo.")

        self.abrir_simulador()

        self.clicar_botao("Simular sem BZU")
        self.esperar_simulacoes_salvas(1)

        self.clicar_botao("Simular com BZU")
        self.esperar_simulacoes_salvas(2)
        self.pausa(2)

        # agora o botão do comparativo fica habilitado
        self.clicar_botao(BOTAO_COMPARATIVO)

        self.wait.until(EC.url_contains("/comparativo/"))
        h1 = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        self.assertIn("Comparativo das Simulações", h1.text)

        cabecalhos = [
            th.text.strip() for th in self.driver.find_elements(By.TAG_NAME, "th")
        ]
        self.assertEqual(cabecalhos, ["Indicador", "Sem BZU", "Com BZU"])

        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Tempo de parada", body)
        self.assertIn("Impacto na produtividade", body)
        self.assertIn("Produtividade comprometida", body)
        self.assertIn("Impacto reduzido pela intervenção preventiva", body)
        self.assertIn("Comparação realizada com sucesso!", body)

        self.pausa(5)