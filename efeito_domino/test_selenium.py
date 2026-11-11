"""
Testes E2E (Selenium) - app efeito_domino
  US01 - Acesso e início da experiência do simulador
  US02 - Execução da simulação sem monitoramento
  US03 - Transição para o cenário de monitoramento (com BZU)
  US04 - Execução da simulação com monitoramento (alerta + opções de decisão)
  US05 - Inspeção de telemetria e linha do tempo das máquinas
  US06 - Tomada de decisão preventiva ("Acionar manutenção")

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


# =============================================================================
# US04, US05 e US06 - abas "Tomar decisão" e "Linha de Produção" do simulador
# =============================================================================
class BaseSimulador(BaseTestCase):
    """Utilitários das abas do simulador (sem testes próprios)."""

    def abrir_aba_decisao(self):
        self.abrir_simulador()
        self.clicar_botao("Tomar decisão")
        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[contains(., 'Tomada de decisão preventiva')]")
            )
        )

    def iniciar_simulacao_com_bzu(self):
        """Abre a aba de decisão e dispara o alerta de anomalia."""
        self.abrir_aba_decisao()
        self.clicar_botao("Iniciar simulação com BZU")
        return self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".us4-box.alerta"))
        )

    def abrir_aba_linha(self):
        self.abrir_simulador()
        self.clicar_botao("Linha de Produção")
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".pl-line"))
        )

    def linha_do_tempo_decisao(self):
        """Textos da 'Linha do tempo da intervenção' (US04/US06)."""
        return [
            p.text
            for p in self.driver.find_elements(By.CSS_SELECTOR, ".us4-tl p")
        ]


class Teste_04_US04_AlertaComOpcoesDeDecisao(BaseSimulador):
    """US04: alerta de anomalia em tempo real com opções de decisão."""

    def test_09_deve_exibir_aba_de_decisao_com_monitoramento_ativo(self):
        print("US04 - Teste 09: Aba de decisão com monitoramento ATIVO.")

        self.abrir_aba_decisao()

        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Status do monitoramento", body)
        self.assertIn("ATIVO", body)
        self.assertTrue(
            self.driver.find_element(
                By.XPATH, "//button[normalize-space(.)='Iniciar simulação com BZU']"
            ).is_displayed()
        )
        # antes de iniciar não existe alerta
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".us4-box.alerta"), []
        )

        self.pausa(2)

    def test_10_deve_exibir_alerta_de_anomalia_com_tres_opcoes(self):
        print("US04 - Teste 10: Alerta de anomalia e opções de decisão.")

        alerta = self.iniciar_simulacao_com_bzu()

        self.assertIn("Anomalia detectada", alerta.find_element(By.TAG_NAME, "h3").text)
        self.assertIn("Máquina 02", alerta.find_element(By.TAG_NAME, "h3").text)
        self.assertIn(
            "Aguardando decisão do operador",
            alerta.find_element(By.CSS_SELECTOR, ".us4-status").text,
        )

        opcoes = [
            b.text.strip()
            for b in alerta.find_elements(By.CSS_SELECTOR, ".us4-acoes button")
        ]
        self.assertEqual(
            opcoes, ["Ignorar alerta", "Verificar dados", "Acionar manutenção"]
        )

        # linha do tempo já registra a detecção
        historico = self.linha_do_tempo_decisao()
        self.assertIn("Monitoramento BZU ativo.", historico[0])
        self.assertIn("Sensor detectou anomalia na Máquina 02.", historico[1])

        self.pausa(3)

    def test_11_deve_verificar_dados_da_maquina_sem_encerrar_o_alerta(self):
        print("US04 - Teste 11: 'Verificar dados' mostra telemetria da Máquina 02.")

        alerta = self.iniciar_simulacao_com_bzu()
        self.clicar_botao("Verificar dados")

        painel = self.wait.until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, ".us4-box.alerta .pl-panel")
            )
        )
        self.assertIn("Máquina 02", painel.find_element(By.TAG_NAME, "h3").text)

        rotulos = [
            s.text.strip()
            for s in painel.find_elements(By.CSS_SELECTOR, ".pl-ind-head span")
        ]
        self.assertEqual(rotulos, ["Temperatura", "Vibração", "Eficiência"])

        # a decisão continua pendente e a consulta fica registrada
        self.assertIn(
            "Aguardando decisão do operador",
            alerta.find_element(By.CSS_SELECTOR, ".us4-status").text,
        )
        self.assertIn(
            "Operador consultou os dados da Máquina 02.",
            self.linha_do_tempo_decisao()[-1],
        )

        self.pausa(3)

    def test_12_deve_propagar_falha_ao_ignorar_alerta(self):
        print("US04 - Teste 12: Ignorar o alerta propaga a falha.")

        self.iniciar_simulacao_com_bzu()
        self.clicar_botao("Ignorar alerta")

        resultado = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.danger"))
        )
        self.assertIn("O alerta foi ignorado", resultado.text)
        self.assertIn("toda a cadeia", resultado.text)

        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".us4-box.alerta"), []
        )
        self.assertIn(
            "Alerta ignorado pelo operador.", self.linha_do_tempo_decisao()[-2]
        )

        # sem resolver, o comparativo final continua bloqueado
        botao = self.driver.find_element(
            By.XPATH, "//button[normalize-space(.)='Ver comparativo final']"
        )
        self.assertFalse(botao.is_enabled())

        self.pausa(3)

    def test_13_deve_permitir_tentar_novamente_apos_ignorar(self):
        print("US04 - Teste 13: 'Tentar novamente' reinicia a simulação.")

        self.iniciar_simulacao_com_bzu()
        self.clicar_botao("Ignorar alerta")
        self.clicar_botao("Tentar novamente")

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space(.)='Iniciar simulação com BZU']")
            )
        )
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".dfs-result"), []
        )

        self.pausa(2)


class Teste_05_US05_InspecaoTelemetriaMaquinas(BaseSimulador):
    """US05: selecionar máquina e ver telemetria + linha do tempo."""

    MAQUINAS = [
        "Máquina 01 - Recepção",
        "Máquina 02 - Processamento",
        "Máquina 03 - Montagem",
        "Máquina 04 - Expedição",
    ]

    def test_14_deve_listar_maquinas_da_linha_de_producao(self):
        print("US05 - Teste 14: Quatro máquinas e dica de seleção.")

        self.abrir_aba_linha()

        nomes = [
            b.text.strip()
            for b in self.driver.find_elements(By.CSS_SELECTOR, ".pl-machine")
        ]
        self.assertEqual(nomes, self.MAQUINAS)

        self.assertIn(
            "Clique em uma máquina para ver os dados de telemetria.",
            self.driver.find_element(By.CSS_SELECTOR, ".pl-hint").text,
        )
        self.assertEqual(self.driver.find_elements(By.CSS_SELECTOR, ".pl-panel"), [])

        self.pausa(2)

    def test_15_deve_exibir_telemetria_da_maquina_selecionada(self):
        print("US05 - Teste 15: Telemetria da Máquina 02.")

        self.abrir_aba_linha()
        self.clicar_botao("Máquina 02 - Processamento")

        painel = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".pl-panel"))
        )
        titulo = painel.find_element(By.TAG_NAME, "h3").text
        self.assertIn("Máquina 02", titulo)
        self.assertIn("Processamento", titulo)

        rotulos = [
            s.text.strip()
            for s in painel.find_elements(By.CSS_SELECTOR, ".pl-ind-head span")
        ]
        self.assertEqual(rotulos, ["Temperatura", "Vibração", "Eficiência", "Uptime"])

        # a máquina escolhida fica destacada e a dica some
        ativas = self.driver.find_elements(By.CSS_SELECTOR, ".pl-machine.active")
        self.assertEqual(len(ativas), 1)
        self.assertIn("Máquina 02", ativas[0].text)
        self.assertEqual(self.driver.find_elements(By.CSS_SELECTOR, ".pl-hint"), [])

        self.pausa(3)

    def test_16_deve_exibir_limites_de_cada_indicador(self):
        print("US05 - Teste 16: Regras/limites de temperatura, vibração e eficiência.")

        self.abrir_aba_linha()
        self.clicar_botao("Máquina 01 - Recepção")
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".pl-panel"))
        )

        rodapes = [
            e.text for e in self.driver.find_elements(By.CSS_SELECTOR, ".pl-ind-foot")
        ]
        regras = ["máx. 80 °C", "máx. 5.0 mm/s", "mín. 85%", "meta 99%"]
        self.assertEqual(len(rodapes), len(regras))
        for rodape, regra in zip(rodapes, regras):
            self.assertIn(regra, rodape)
            self.assertTrue(
                "Dentro do normal" in rodape or "Acima do limite normal" in rodape,
                f"Indicador sem status: {rodape}",
            )

        self.pausa(3)

    def test_17_deve_trocar_de_maquina(self):
        print("US05 - Teste 17: Trocar a máquina selecionada.")

        self.abrir_aba_linha()

        self.clicar_botao("Máquina 01 - Recepção")
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".pl-panel h3"), "Máquina 01"
            )
        )

        self.clicar_botao("Máquina 04 - Expedição")
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".pl-panel h3"), "Máquina 04"
            )
        )

        ativas = self.driver.find_elements(By.CSS_SELECTOR, ".pl-machine.active")
        self.assertEqual(len(ativas), 1)
        self.assertIn("Máquina 04", ativas[0].text)

        self.pausa(3)

    def test_18_deve_atualizar_linha_do_tempo_em_tempo_real(self):
        print("US05 - Teste 18: Linha do tempo cresce a cada nova leitura.")

        self.abrir_aba_linha()
        self.clicar_botao("Máquina 03 - Montagem")

        hist = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".pl-hist"))
        )
        self.assertIn("Linha do tempo", hist.text)

        itens = lambda d: d.find_elements(By.CSS_SELECTOR, ".pl-hist li")

        # a tela consulta a API a cada 2 s: sem recarregar, surgem novas linhas
        self.wait.until(lambda d: len(itens(d)) >= 1)
        self.driver.execute_script("window.marcadorSemRecarga = 'ok';")
        self.wait_longo.until(lambda d: len(itens(d)) >= 3)

        for li in itens(self.driver):
            self.assertTrue(
                "Operação normal" in li.text or "Valores acima do limite" in li.text,
                f"Entrada inesperada na linha do tempo: {li.text}",
            )
        self.assertEqual(
            self.driver.execute_script("return window.marcadorSemRecarga;"), "ok"
        )

        self.pausa(3)


class Teste_06_US06_TomadaDeDecisaoPreventiva(BaseSimulador):
    """US06: escolher 'Acionar manutenção' ao receber o alerta."""

    def test_19_deve_acionar_manutencao_e_estabilizar_a_maquina(self):
        print("US06 - Teste 19: Acionar manutenção resolve o alerta.")

        self.iniciar_simulacao_com_bzu()
        self.clicar_botao("Acionar manutenção")

        resultado = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.safe"))
        )
        self.assertIn("Intervenção preventiva registrada", resultado.text)
        self.assertIn("Máquina 02 estabilizada", resultado.text)
        self.assertIn("Impacto reduzido", resultado.text)
        self.assertIn("Tempo economizado", resultado.text)
        self.assertIn(
            "Resultado da intervenção: Propagação de falha evitada", resultado.text
        )

        # alerta encerrado e nada de mensagem de prejuízo
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".us4-box.alerta"), []
        )
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".dfs-result.danger"), []
        )

        self.pausa(3)

    def test_20_deve_registrar_a_intervencao_na_linha_do_tempo(self):
        print("US06 - Teste 20: Linha do tempo da intervenção.")

        self.iniciar_simulacao_com_bzu()
        self.clicar_botao("Acionar manutenção")
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.safe"))
        )

        historico = self.linha_do_tempo_decisao()
        self.assertEqual(len(historico), 4)
        self.assertIn("Monitoramento BZU ativo.", historico[0])
        self.assertIn("Sensor detectou anomalia na Máquina 02.", historico[1])
        self.assertIn("Manutenção preventiva acionada na Máquina 02.", historico[2])
        self.assertIn("Operação da máquina estabilizada.", historico[3])

        self.pausa(3)

    def test_21_deve_liberar_comparativo_final_somente_apos_resolver(self):
        print("US06 - Teste 21: Comparativo final liberado após a manutenção.")

        self.iniciar_simulacao_com_bzu()

        botao = self.driver.find_element(
            By.XPATH, "//button[normalize-space(.)='Ver comparativo final']"
        )
        self.assertFalse(botao.is_enabled(), "Deveria estar bloqueado no alerta.")

        self.clicar_botao("Acionar manutenção")

        # o React pode recriar o botão: procura de novo a cada verificação
        xpath = "//button[normalize-space(.)='Ver comparativo final']"
        self.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        ).click()
        comparativo = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-compare"))
        )
        self.assertIn("Sem BZU: 4 de 4", comparativo.text)
        self.assertIn("Com BZU: 0 de 4", comparativo.text)

        self.pausa(4)

    def test_22_deve_reiniciar_simulacao_apos_a_intervencao(self):
        print("US06 - Teste 22: Reiniciar simulação volta ao estado inicial.")

        self.iniciar_simulacao_com_bzu()
        self.clicar_botao("Acionar manutenção")
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.safe"))
        )

        self.clicar_botao("Reiniciar simulação")

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[normalize-space(.)='Iniciar simulação com BZU']")
            )
        )
        self.assertEqual(self.driver.find_elements(By.CSS_SELECTOR, ".dfs-result"), [])
        self.assertEqual(self.driver.find_elements(By.CSS_SELECTOR, ".us4-tl"), [])

        self.pausa(2)

    def test_23_deve_evitar_a_falha_ao_tentar_de_novo_e_acionar_manutencao(self):
        print("US06 - Teste 23: Ignorar, tentar novamente e então acionar manutenção.")

        self.iniciar_simulacao_com_bzu()
        self.clicar_botao("Ignorar alerta")
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.danger"))
        )

        self.clicar_botao("Tentar novamente")
        self.clicar_botao("Iniciar simulação com BZU")
        self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".us4-box.alerta"))
        )
        self.clicar_botao("Acionar manutenção")

        resultado = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dfs-result.safe"))
        )
        self.assertIn("Máquina 02 estabilizada", resultado.text)
        self.assertEqual(
            self.driver.find_elements(By.CSS_SELECTOR, ".dfs-result.danger"), []
        )

        self.pausa(3)