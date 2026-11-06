from django.test import override_settings
from django.utils import timezone
from os import link

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager

import time

from forum.models import Pergunta




class BaseTestCase(StaticLiveServerTestCase):
    """
    Classe-base que inicializa e encerra o Chrome em modo headless
    (sem interface gráfica) antes e depois de cada teste.

    StaticLiveServerTestCase sobe um servidor HTTP temporário em uma 
    porta aleatória na própria máquina que está rodando os testes, usando 
    um banco de dados de teste isolado, e disponibiliza self.live_server_url 
    para que o Selenium possa acessá-lo.

    live_server_url aponta sempre para localhost. Ex: http://127.0.0.1:54321
    Esse servidor existe apenas durante a execução dos testes e é destruído 
    logo depois. 

    """
     
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        opts = Options()
        opts.add_argument("--headless")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1280,800")

        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=opts)

        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "driver"):
            cls.driver.quit()
        super().tearDownClass()

    # -------------------------------------------------------------------------
    # Métodos utilitários reutilizados pelos testes
    # -------------------------------------------------------------------------

    def abrir_pagina(self, caminho="/forum/"):
        """Navega para uma URL relativa ao servidor de teste."""
        self.driver.get(self.live_server_url + caminho)

    def criar_pergunta_via_model(
        self,
        titulo="Título de teste",
        detalhe="Detalhe da pergunta de teste.",
        tentativa="Tentativa de solução.",
        usuario="Equipe de engenheiros de testes",
    ):
        """Cria uma Pergunta diretamente no banco — útil para preparar o estado
        do sistema antes de um teste, sem depender da UI de inserção."""
        return Pergunta.objects.create(
            titulo=titulo,
            detalhe=detalhe,
            tentativa=tentativa,
            data_criacao=timezone.now(),
            usuario=usuario,
        )

    def criar_resposta_via_model(self, pergunta, texto="Resposta de teste.", usuario="respondedor"):
        """Cria uma Resposta diretamente no banco."""
        return pergunta.resposta_set.create(
            texto=texto,
            data_criacao=timezone.now(),
            usuario=usuario,
        )

# dica: colocar a numeração dos testes nas classes e métodos indica 
# a ordem de execução (o unittest roda os testes em ordem alfabética).
#  Embora os testes definidos aqui sejam todos independentes
# e possam executar em qualquer ordem, ordenar a execução ajuda a 
# visualizar o processo de testes e a criação do screencast. 
class Teste_01_PaginaInicial(BaseTestCase):
    
    """Testa a listagem de perguntas na página inicial do fórum."""

    def test_01_deve_carregar_pagina_inicial_sem_perguntas(self):
        print("Teste 01: Visualização da página inicial sem perguntas.")

        # abre a página inicial do fórum
        self.abrir_pagina("/forum/")

        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

          # verifica se aparece a mensagem de nenhuma pergunta disponível
        self.assertIn("Nenhuma pergunta disponível", body.text)
       
      
        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido
        

    def test_02_deve_carregar_pagina_inicial_com_perguntas(self):

        print("Teste 02: Visualização da página inicial com uma pergunta cadastrada.")
        # Cria uma pergunta no banco de dados
        self.criar_pergunta_via_model()

        # abre a página inicial do fórum
        self.abrir_pagina("/forum/")

        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # verifica se a pergunta criada aparece na página
        self.assertIn("Título de teste", body.text)

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido


    def test_03_deve_carregar_pagina_inicial_com_tres_perguntas_cadastradas(self):
       
        print("Teste 03: Visualização da página inicial com três perguntas cadastradas.")
        
        titulos = [
            "Como usar list comprehension em Python?",
            "O que é uma closure em JavaScript?",
            "Como funciona o JOIN no SQL?",
        ]
        
        # Cria 3 perguntas diretamente no banco.
        for t in titulos:
            self.criar_pergunta_via_model(titulo=t)

        # abre a página inicial
        self.abrir_pagina("/forum/")

        # verifica se os 3 títulos aparecem como links.
        links = self.driver.find_elements(By.CSS_SELECTOR, "ul li a")
        textos_encontrados = [l.text.strip() for l in links]

        for titulo in titulos:
            self.assertIn(titulo, textos_encontrados,
                          f"Título '{titulo}' não encontrado na listagem.")

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido


class Teste_02_CriacaoPergunta(BaseTestCase):

    """Testa a criação de perguntas no fórum."""

    def test_04_deve_criar_pergunta(self):
        print("Teste 04: Criação de pergunta e visualização da mesma.")
        
        # abre a página de criação de pergunta
        self.abrir_pagina("/forum/inserir/")
 
        # pega os campos do formulário de criação de pergunta
        titulo = self.wait.until(
            EC.presence_of_element_located((By.NAME, "titulo"))
        )
        detalhe = self.wait.until(
            EC.presence_of_element_located((By.NAME, "detalhe"))
        )

        tentativa = self.wait.until(
            EC.presence_of_element_located((By.NAME, "tentativa"))
        )

        # preenche os dados da pergunta.
        titulo.send_keys("Teste 04: Como usar o Selenium com Django?")

        detalhe.send_keys("Podem me indicar tutoriais ou exemplos de uso do Selenium para testes em Django?")

        tentativa.send_keys("Não tentei nada ainda.")

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido
        
        # clica no botão de submit do formulário para gravar a pergunta
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # espera a página recarregar e exibir conteúdo
        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # verifica se o título da pergunta criada aparece na página
        self.assertIn("Como usar o Selenium com Django?", body.text)
        
        time.sleep(10)  # Apenas para visualizar o teste, pode ser removido

    def test_05_deve_criar_pergunta_e_acessar_pergunta_criada_pela_pagina_principal_e_exibir_detalhes_pergunta(self):
        print("Teste 05: Criação de pergunta, acesso pela página principal e visualização dos seus detalhes.")
        
        # acessa página de criação de pergunta
        self.abrir_pagina("/forum/inserir/")

        titulo = self.wait.until(
            EC.presence_of_element_located((By.NAME, "titulo"))
        )
        detalhe = self.wait.until(
            EC.presence_of_element_located((By.NAME, "detalhe"))
        )

        tentativa = self.wait.until(
            EC.presence_of_element_located((By.NAME, "tentativa"))
        )

        # preenche campos.
        titulo.send_keys("Teste 05: Como criar jogos no Unity?")

        detalhe.send_keys("Podem me ajudar por favor?")

        tentativa.send_keys("Ainda não tentei nada, quero muito começar a programar jogos.")

        time.sleep(2)  # Apenas para visualizar o teste, pode ser removido

        # grava a pergunta
        self.driver.find_element(By.TAG_NAME, "form").submit()

        # espera redirecionamento/listagem
        self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(3)  # Apenas para visualizar o teste, pode ser removido

        # vai para página inicial
        self.abrir_pagina("/forum/")

        # clica no link da pergunta criada para acessar detalhes
        link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Teste 05: Como criar jogos no Unity?"))
        )

        time.sleep(4)  # Apenas para visualizar o teste, pode ser removido

        link.click()

        body = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(10)  # Apenas para visualizar o teste, pode ser removido

        self.assertIn("Podem me ajudar por favor?", body.text)
