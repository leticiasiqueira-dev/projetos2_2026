from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from atuadores.models import Atuador
from project.selenium_base import BaseTestCase

PERMISSAO = "enviar_comando_atuador"


class Teste_08_US08_ComandosAtuadores(BaseTestCase):
    """US08: operador autorizado envia comandos remotos aos atuadores."""

    def criar_atuador(self, nome="Exaustor Linha 1", tipo="EXAUSTOR"):
        return Atuador.objects.create(
            nome=nome, tipo=tipo, topico_mqtt=f"fabrica/{nome.replace(' ', '_').lower()}"
        )

    def logar_como_operador(self):
        operador = self.criar_usuario("operador", permissoes=[PERMISSAO])
        self.fazer_login(operador)

    def test_01_deve_redirecionar_visitante_para_login(self):
        print("US08 - Teste 01: Visitante sem login vai para a tela de login.")

        self.abrir_pagina("/atuadores/")

        self.wait.until(EC.url_contains("/admin/login/"))

        self.pausa(2)

    def test_02_deve_exibir_painel_com_atuadores(self):
        print("US08 - Teste 02: Painel lista atuadores e estado atual.")

        self.criar_atuador()
        self.logar_como_operador()
        self.abrir_pagina("/atuadores/")

        h1 = self.wait.until(EC.visibility_of_element_located((By.TAG_NAME, "h1")))
        self.assertIn("Controle de Atuadores", h1.text)

        card = self.driver.find_element(By.CSS_SELECTOR, "section.card")
        self.assertIn("Exaustor Linha 1", card.find_element(By.TAG_NAME, "h2").text)
        self.assertIn("DESLIGADO", card.find_element(By.CSS_SELECTOR, ".estado").text)

        self.pausa(3)

    def test_03_deve_enviar_comando_ligar_apos_confirmacao(self):
        print("US08 - Teste 03: LIGAR exaustor com confirmação.")

        self.criar_atuador()
        self.logar_como_operador()
        self.abrir_pagina("/atuadores/")

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-command='LIGAR']"))
        ).click()

        # modal de confirmação
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "modalConfirmacao"))
        )
        self.assertIn(
            "Deseja realmente LIGAR o atuador?",
            self.driver.find_element(By.ID, "textoConfirmacao").text,
        )
        self.pausa(2)

        self.driver.find_element(By.ID, "confirmar").click()

        # feedback do servidor aparece na tela
        self.wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".mensagem"), "Comando recebido"
            )
        )
        self.wait.until(
            EC.invisibility_of_element_located((By.ID, "modalConfirmacao"))
        )

        self.pausa(3)

    def test_04_deve_cancelar_comando_sem_enviar(self):
        print("US08 - Teste 04: Cancelar fecha o modal e não envia nada.")

        self.criar_atuador()
        self.logar_como_operador()
        self.abrir_pagina("/atuadores/")

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-command='DESLIGAR']"))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "modalConfirmacao"))
        )

        self.driver.find_element(By.ID, "cancelar").click()

        self.wait.until(
            EC.invisibility_of_element_located((By.ID, "modalConfirmacao"))
        )
        self.assertEqual(
            self.driver.find_element(By.CSS_SELECTOR, ".mensagem").text, ""
        )

        self.pausa(2)

    def test_05_deve_negar_comando_para_usuario_sem_permissao(self):
        print("US08 - Teste 05: Usuário sem permissão não consegue atuar.")

        self.criar_atuador()
        sem_permissao = self.criar_usuario("visitante", permissoes=[])
        self.fazer_login(sem_permissao)
        self.abrir_pagina("/atuadores/")

        self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-command='LIGAR']"))
        ).click()
        self.wait.until(
            EC.visibility_of_element_located((By.ID, "modalConfirmacao"))
        )
        self.driver.find_element(By.ID, "confirmar").click()

        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".mensagem"), "Erro")
        )
        self.assertNotIn(
            "Comando recebido",
            self.driver.find_element(By.CSS_SELECTOR, ".mensagem").text,
        )

        self.pausa(3)

    def test_06_deve_exibir_mensagem_quando_nao_ha_atuadores(self):
        print("US08 - Teste 06: Painel sem atuadores cadastrados.")

        self.logar_como_operador()
        self.abrir_pagina("/atuadores/")

        vazio = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".vazio"))
        )
        self.assertIn("Nenhum atuador cadastrado", vazio.text)

        self.pausa(2)