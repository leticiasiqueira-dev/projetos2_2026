# Modelagem dos Ambientes de Desenvolvimento e Deploy: IoTech

> Projetos 2 – Grupo 12 · Central de Ocorrências IoT (Django)

## 1. Visão geral do fluxo

O código do sistema passa por quatro etapas até chegar ao usuário final:

1. **Desenvolvimento:** cada integrante programa e testa na própria máquina.
2. **Repositório (GitHub):** o código é enviado por `git push` e integrado à branch `main` por meio de Pull Request.
3. **CI/CD (GitHub Actions):** a cada integração, um pipeline automático instala as dependências e roda os testes. Se algum teste falhar, o código volta para o desenvolvimento para correção.
4. **Homologação e produção:** com os testes aprovados, a versão vai primeiro para o ambiente de homologação, onde o grupo valida. Após a aprovação, segue para produção, onde os usuários finais acessam.

## 2. Ambiente de desenvolvimento

Ambiente onde o grupo escreve e testa o código antes de enviá-lo ao repositório. Roda na máquina de cada integrante e é composto por:

- **Editor de código:** VS Code.
- **Linguagem e framework:** Python com Django, em um ambiente virtual (`venv`).
- **Banco de dados:** SQLite local (`db.sqlite3`).
- **Servidor de desenvolvimento:** `python manage.py runserver`, acessado em `127.0.0.1:8000`.
- **Navegador:** usado para os testes manuais das páginas.
- **Controle de versão:** Git local, sincronizado com o GitHub.
- **Apoio ao time:** Figma para protótipos e design; Slack e WhatsApp para comunicação.

## 3. Ambiente de produção (implantação)

Ambiente onde o sistema fica disponível para uso real, hospedado em um provedor de nuvem. Seus componentes são:

- **Servidor web:** Render.
- **Aplicação:** Django (IoTech), executado pelo Gunicorn.
- **Arquivos estáticos:** CSS, JavaScript e imagens.
- **Banco de dados:** SQL.

- **Usuários:** pelo navegador ou celular, via HTTPS (porta 443).
- **Sensores IoT da BZU:** a definir
