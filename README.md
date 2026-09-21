# 🔗 IoTech
 
### Transformando dados de IoT em decisões de negócio mais inteligentes
*Projeto desenvolvido em parceria com a **BzuTech**, no contexto da disciplina de Projetos (2º período) — CESAR School.*

## 📌 Descrição do projeto

Este projeto tem como objetivo explorar o uso da Internet das Coisas (IoT), 
com foco em sensoriamento e nos benefícios proporcionados por essa tecnologia.

A proposta da BZU TECH é aplicar sensores e dispositivos conectados para coletar e transmitir dados do ambiente em tempo real. 
A partir da análise dessas informações brutas, a solução viabiliza o monitoramento contínuo, a automação de processos e o aumento
da visibilidade operacional, fornecendo suporte estratégico para a tomada de decisões.

Ao longo do projeto, serão analisadas aplicações de IoT em diferentes contextos,
destacando benefícios como aumento da eficiência, redução de custos, 
monitoramento em tempo real, automação de processos e melhor utilização 
dos recursos disponíveis.

<div align="center">

 `🌐 Sobre` · `🧭 Como Funciona` · `🛰️ Stack` · `📶 Ciclos de Entrega` · `⚙️ Rodando` · `👥 Equipe`

 </div>

## 🌐 Sobre o Projeto
Boa parte das empresas ainda opera com uma visão parcial do próprio negócio: informações sobre máquinas, processos, infraestrutura e ambiente de trabalho não são acompanhadas de forma contínua, o que dificulta identificar gargalos e antecipar problemas.
 
Este projeto propõe explorar de que forma a **Internet das Coisas (IoT)** pode preencher essa lacuna, permitindo captar dados operacionais em tempo real e convertê-los em ganhos concretos de produtividade e automação — traduzindo tecnologia em uma experiência de gestão simples e acessível para empresas que ainda não enxergam IoT como ferramenta de decisão.

## 🧭 Como Funciona

 - *[a definir]*
 
---

## 🛰️ Stack do Projeto
 
| Camada | Ferramentas |
|---|---|
| 🖥️ **Produto** | *Simulador de "efeito dominó"* |
| 🎨 **Design** | Figma (UI, protótipo e design system) · *[outras ferramentas a definir]* |
| 🗂️ **Gestão & Versionamento** | Git / GitHub · Jira |
 
---

## 🛠️ Tecnologias Usadas
 
**Produto**
- *Simulador de "efeito dominó"*
**Design**
- Figma (UI, protótipo e design system)
- *[Outras ferramentas de pesquisa/design, a definir]*
**Gestão & Versionamento**
- Git / GitHub
- Jira

---

## 📶 Ciclos de Entrega

### 📦 Entrega 01

Análise de competidores e definição inicial dos requisitos do produto.

### Artefatos

- 📄 [Documento de análise de competidores e benchmark](https://github.com/leticiasiqueira-dev/projetos2_2026/blob/main/relatorioDeAnaliseDeCompetidores.md)
- 🖼️ Print do quadro da sprint:<img width="1917" height="862" alt="image" src="https://github.com/user-attachments/assets/6710acbc-962f-4f3e-9fe9-451c6e13b1a6"/>

### 📦 Entrega 02

Implementação da infraestrutura básica da aplicação e deploy em produção.

### Artefatos

- 🎥 [Screencast do uso do sistema](#)
- 🎥 [Screencast de explicação do código](#)
- 🖼️ [Print do bug tracker](#)
- 🖼️ [Print do quadro da Sprint 02](#)

### Entrega 03

Definição das histórias de usuário e implementação das primeiras histórias selecionadas.
 
**Artefatos / Screenshots:**

- 📄 [Documento de histórias de usuário](#)
- 🖼️ [Print do backlog (Jira)](#)
- 🎥 [Screencast das histórias implementadas](#)
- 🎥 [Screencast de explicação do código](#)
- 🖼️ [Print do quadro da Sprint 03](#)
  
### Entrega 04
 
Implementação das histórias restantes, testes automatizados e pipeline de CI/CD.
 
**Artefatos / Screenshots:**
- 🎥 [Screencast do deployment das novas histórias](#)
- 🧪 [Screencast dos testes E2E (Selenium)](#)
- 🔁 [Screencast do processo de CI/CD](#)
- 🎥 [Screencast de explicação do código](#)
- 🖼️ [Print do quadro da Sprint 04](#)

---
 Deploy

A aplicação está publicada em: **COLE_AQUI_A_URL_DO_DEPLOY**

### Como acessar

1. Abra a URL acima no navegador. A raiz (`/`) redireciona para a **Central de Ocorrências** (`/forum/`).
2. Para registrar uma ocorrência, use **Registrar ocorrência** no menu (`/forum/inserir/`). Não é necessário criar conta: quem não está autenticado aparece como *anônimo*.
3. Abra uma ocorrência para ver os diagnósticos, adicionar um novo ou marcar um como útil.
4. Para ver o simulador, acesse **Sobre o projeto** (`/efeito_domino/`) e clique em **Explorar simulador**. Ele exibe a ocorrência mais recente registrada.
5. A área administrativa fica em `/admin/` e exige um superusuário. As credenciais não são públicas e podem ser solicitadas à equipe.

---

## ⚙️ Como rodar o projeto

**Pré-requisitos:** Python 3.12 ou superior e Git.

1. Clone o repositório:
```bash
git clone https://github.com/leticiasiqueira-dev/projetos2_2026.git
cd projetos2_2026
```
2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Configure as variáveis de ambiente. Copie o modelo e edite o `.env`:
```bash
cp .env.example .env            # Windows: copy .env.example .env
```
```env
SECRET_KEY=troque-por-uma-chave-secreta
ENVIRONMENT=development
```
5. Crie as tabelas do banco (SQLite local):
```bash
python manage.py migrate
```
6. Execute o projeto:
```bash
python manage.py runserver
```
Acesse http://127.0.0.1:8000/

Opcional: para usar o `/admin/`, crie um superusuário com `python manage.py createsuperuser`.

---
## 🐞 Bug tracker

Bugs, melhorias e tarefas técnicas são registrados nas [Issues do GitHub](https://github.com/leticiasiqueira-dev/projetos2_2026/issues). Os commits são feitos diretamente na `main`, com frequência semanal no mínimo, e referenciam a issue correspondente (ex.: `Corrige XSS no simulador (fixes #1)`).

---

## 👥 Membros da equipe

### Ciência da Computação
 
| Nome Completo | E-mail Institucional |
|---|---|
| Letícia Almeida Abreu de Siqueira  | laas2@cesar.school |
| Letícia Dornas de Araújo  | lda2@cesar.school |
| Maria Júlia Oliveira Dionísio  | mjod@cesar.school |
| Maria Monalysa da Silva  | mms2@cesar.school |
| Manuela Brayner Medeiros de Araújo  | mbma3@cesar.school |
| Matheus Araújo Guilhermino  | mag3@cesar.school |
| Milena Siqueira Araújo  | msa4@cesar.school |
| Rafaela Dubeux Godoy  | rdg@cesar.school |
| Renata Rodrigues Bezerra  | rrb2@cesar.school |

 
### Design
 
| Nome Completo | E-mail Institucional |
|---|---|
| Artur Henrique Ribeiro Câmara de Oliveira  | ahrco@cesar.school |
| Cora Jordão Magri | cjm@cesar.school |
| Luana Malinconico Pereira | lmp3@cesar.school |
| Mateus Rodrigues de Lira Assunção | mrla@cesar.school |

## 🔄 Ex-Integrantes
 
<!-- Preencher somente se houve mudança na composição do grupo. Caso contrário, remover ou indicar "Sem alterações no grupo". -->
 
| Nome Completo | E-mail Institucional | Entrada | Saída |
|---|---|---|---|
|  |  |  |  |
 
---
 
## 🤝 Parceiro
 
**BzuTech** — tecnologia de IoT voltada à eficiência operacional das empresas.
 
## 📡 Painéis de Acompanhamento
 
- 🗂️ **Jira:** [link do quadro](https://projetos2ccdsg.atlassian.net/jira/software/projects/SCRUM/boards/1?filter=&groupBy=subtask)
- 🐞 **Bug tracker:** [GitHub Issues](https://github.com/leticiasiqueira-dev/projetos2_2026/issues)
- 🎨 **Figma:** [link do protótipo](#)

## 📄 Licença
 
*[Preencher conforme o projeto avançar]*
