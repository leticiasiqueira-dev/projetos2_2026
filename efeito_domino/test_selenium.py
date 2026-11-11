"""
Testes E2E (Selenium) - app efeito_domino
  US01 - Acesso e início da experiência do simulador
  US02 - Execução da simulação sem monitoramento
  US03 - Transição para o cenário de monitoramento (com BZU)

Dica: a numeração nas classes/métodos define a ordem de execução
(o unittest roda em ordem alfabética).
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from project.selenium_base import BaseTestCase


class Teste_01_US01_PaginaInicial(BaseTestCase):
    """US01: página inicial com apresentação dos conceitos e botão de início."""

    def test_01_deve_exibir_apresentacao_dos_conceitos(self):
        print("US01 - Teste 01: Apresentação dos conceitos na página inicial.")

        self.abrir_pagina("/efeito_domino/")

        h1 = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        self.assertIn("Quando uma máquina para", h1.text)

        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Máquina → Produção → Pedido → Cliente → Prejuízo", body)
        self.assertIn("tecnologia IoT", body)
        self.assertIn("BZU", self.driver.title)

        self.pausa(3)

    def test_02_deve_exibir_botao_de_inicio(self):
        print("US01 - Teste 02: Botão 'Explorar simulador' visível.")

        self.abrir_pagina("/efeito_domino/")

        botao = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "a.botao"))
        )
        self.assertIn("Explorar simulador", botao.text)

        self.pausa(2)

    def test_03_deve_iniciar_simulador_ao_clicar_no_botao(self):
        print("US01 - Teste 03: Clique no botão leva ao simulador.")

        self.abrir_pagina("/efeito_domino/")

        self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Explorar simulador"))
        ).click()

        self.wait.until(EC.url_contains("/efeito_domino/simulador/"))
        self.wait_longo.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[contains(., 'Simulador de efeito dominó')]")
            )
        )

        self.pausa(3)


class Teste_02_US02_SimulacaoSemMonitoramento(BaseTestCase):
    """US02: simulação sem BZU mostra a falha se propagando pela cadeia."""

    def test_04_deve_exibir_botoes_de_simulacao(self):
        print("US02 - Teste 04: Botões de simulação disponíveis.")

        self.abrir_simulador()

        for texto in ["Simular sem BZU", "Simular com BZU", "Reiniciar"]:
            botao = self.driver.find_element(
                By.XPATH, f"//button[normalize-space(.)='{texto}']"
            )
            self.assertTrue(botao.is_displayed(), f"Botão '{texto}' não visível.")

        self.pausa(2)

    def test_05_deve_executar_simulacao_sem_monitoramento(self):
        print("US02 - Teste 05: Falha em cadeia sem monitoramento IoT.")

        self.abrir_simulador()
        botao = self.clicar_botao("Simular sem BZU")

        # enquanto roda, o botão fica desabilitado
        self.wait.until(lambda d: not botao.is_enabled())

        # ao final aparece a mensagem de prejuízo em toda a cadeia
        resultado = self.wait_longo.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.danger"))
        )
        self.assertIn("Sem monitoramento", resultado.text)

        # todas as etapas da cadeia foram afetadas (dominós caídos)
        total = len(self.driver.find_elements(By.CSS_SELECTOR, ".dfs-tile"))
        caidos = len(self.driver.find_elements(By.CSS_SELECTOR, ".dfs-tile.fell"))
        self.assertGreater(total, 1)
        self.assertEqual(total, caidos, "Nem todas as etapas caíram.")

        # sem BZU não existe alerta de detecção
        self.assertEqual(self.driver.find_elements(By.CSS_SELECTOR, ".dfs-alert"), [])

        self.pausa(4)

    def test_06_deve_reiniciar_simulacao(self):
        print("US02 - Teste 06: Reiniciar limpa o resultado.")

        self.abrir_simulador()
        self.clicar_botao("Simular sem BZU")
        self.wait_longo.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.danger"))
        )

        self.clicar_botao("Reiniciar")

        self.wait.until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".dfs-result"))
        )
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".dfs-tile.fell"), []
        )

        self.pausa(2)


class Teste_03_US03_CenarioComMonitoramento(BaseTestCase):
    """US03: cenário com BZU - alerta antecipado interrompe a cascata."""

    def test_07_deve_executar_simulacao_com_monitoramento(self):
        print("US03 - Teste 07: Cenário com BZU detecta e resolve na origem.")

        self.abrir_simulador()
        self.clicar_botao("Simular com BZU")

        # o bloco de alerta aparece assim que o sensor detecta a anomalia
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".dfs-alert"))
        )

        # estado final: manutenção acionada e cascata interrompida
        self.wait_longo.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".dfs-alert-title"), "Manutenção acionada"
            )
        )
        sub = self.driver.find_element(By.CSS_SELECTOR, ".dfs-alert-sub").text
        self.assertIn("cascata foi interrompida na origem", sub)

        resultado = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.safe"))
        )
        self.assertIn("ainda na máquina", resultado.text)

        # nenhuma etapa da cadeia caiu e não há mensagem de prejuízo
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".dfs-tile.fell"), []
        )
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".dfs-result.danger"), []
        )

        self.pausa(4)

    def test_08_deve_transitar_do_cenario_sem_bzu_para_com_bzu(self):
        print("US03 - Teste 08: Transição do cenário sem BZU para com BZU.")

        self.abrir_simulador()

        # 1º cenário: sem monitoramento
        self.clicar_botao("Simular sem BZU")
        self.wait_longo.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.danger"))
        )
        self.pausa(2)

        # 2º cenário: com monitoramento (botão volta a ficar habilitado)
        self.clicar_botao("Simular com BZU")

        # a mensagem de prejuízo some e entra a de problema resolvido
        self.wait_longo.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.safe"))
        )
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".dfs-result.danger"), []
        )

        self.pausa(3)