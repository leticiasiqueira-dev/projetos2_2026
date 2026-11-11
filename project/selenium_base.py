"""
Classe-base compartilhada pelos testes E2E (Selenium) de todos os apps.

Fica na pasta "project" (e NÃO começa com "test") para que o Django não a
trate como arquivo de testes: ela só é importada pelos test_selenium.py de
cada app.

Variáveis de ambiente úteis:
    SELENIUM_HEADLESS=0   abre o Chrome com janela (para assistir/gravar o teste)
    SELENIUM_HEADLESS=1   (padrão) sem janela -> necessário no CI/CD
"""
import os
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

HEADLESS = os.getenv("SELENIUM_HEADLESS", "1") == "1"
SENHA_PADRAO = "senha-de-teste-123"


class BaseTestCase(StaticLiveServerTestCase):
    """
    Sobe um servidor Django temporário (porta aleatória, banco de teste
    isolado) e um Chrome controlado pelo Selenium.
    self.live_server_url aponta para esse servidor. Ex: http://localhost:54321
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        opts = Options()
        if HEADLESS:
            opts.add_argument("--headless=new")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1280,800")
        opts.add_argument("--lang=pt-BR")

        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=opts)

        cls.wait = WebDriverWait(cls.driver, 10)
        # O simulador carrega React/Babel por CDN, então pode demorar mais
        cls.wait_longo = WebDriverWait(cls.driver, 30)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()
        super().tearDownClass()

    def tearDown(self):
        # O mesmo Chrome é reutilizado entre os testes da classe: limpa
        # cookies (sessão/login) para um teste não influenciar o outro.
        try:
            self.driver.delete_all_cookies()
        except Exception:
            pass
        super().tearDown()

    # ------------------------------------------------------------------
    # Utilitários reutilizados pelos testes
    # ------------------------------------------------------------------
    def abrir_pagina(self, caminho="/"):
        """Navega para uma URL relativa ao servidor de teste."""
        self.driver.get(self.live_server_url + caminho)

    def pausa(self, segundos=2):
        """Pausa só para visualizar o teste (ignorada em modo headless)."""
        if not HEADLESS:
            time.sleep(segundos)

    def clicar_botao(self, texto):
        """Clica em um <button> pelo texto exato visível."""
        botao = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//button[normalize-space(.)='{texto}']")
            )
        )
        botao.click()
        return botao

    def abrir_simulador(self):
        """Abre o simulador e espera o React renderizar a tela."""
        self.abrir_pagina("/efeito_domino/simulador/")
        self.wait_longo.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//h2[contains(., 'Simulador de efeito dominó')]")
            )
        )

    def criar_usuario(self, username="operador", permissoes=()):
        """Cria um usuário no banco, com as permissões (codename) indicadas."""
        usuario = get_user_model().objects.create_user(
            username=username, password=SENHA_PADRAO
        )
        for codename in permissoes:
            usuario.user_permissions.add(Permission.objects.get(codename=codename))
        return usuario

    def fazer_login(self, usuario):
        """Autentica o navegador sem digitar no formulário: cria a sessão no
        banco e injeta o cookie de sessão no Chrome."""
        self.client.force_login(usuario)
        cookie = self.client.cookies[settings.SESSION_COOKIE_NAME]
        # o Selenium só aceita cookie depois de abrir uma página do domínio
        self.abrir_pagina("/admin/login/")
        self.driver.add_cookie(
            {"name": settings.SESSION_COOKIE_NAME, "value": cookie.value, "path": "/"}
        )