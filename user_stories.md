# Histórias de Usuário - Plataforma de IoT e Sensoriamento

Este documento apresenta o levantamento das **User Stories** para o sistema de monitoramento IoT e telemetria de sensores, incluindo cenários de teste orientados a comportamento (BDD/Gherkin).

**Módulo principal:** [http://127.0.0.1:8000/forum/](http://127.0.0.1:8000/forum/) (Central de Discussões e Alertas da Comunidade IoT)

---

## US01 - Cadastro e Vinculação de Novo Dispositivo IoT

**Como** engenheiro de automação ou operador do sistema  
**Quero** cadastrar um novo nó sensor (dispositivo IoT) informando seu MAC Address e tipo de sensor  
**Para que** o dispositivo possa transmitir dados telemétricos para a plataforma  

### Cenários de Aceite (BDD)

```gherkin
Cenário: Cadastro de nó sensor com sucesso
  Dado que estou autenticado como operador e na página de dispositivos em "/forum/dispositivos/novo"
  Quando preencho o campo "Nome do Dispositivo" com "Sensor Temperatura Estufa 01"
  E preencho o "MAC Address / UUID" com "AA:BB:CC:11:22:33"
  E seleciono o "Tipo de Sensor" como "Temperatura e Umidade (DHT22)"
  E clico em "Cadastrar Dispositivo"
  Então vejo a mensagem de sucesso "Dispositivo cadastrado com sucesso"
  E o status inicial do dispositivo é exibido como "Aguardando Primeira Leitura"

Cenário: Tentativa de cadastro com MAC Address duplicado
  Dado que já existe um dispositivo cadastrado com o MAC Address "AA:BB:CC:11:22:33"
  Quando tento cadastrar um novo dispositivo utilizando o mesmo MAC Address "AA:BB:CC:11:22:33"
  E clico em "Cadastrar Dispositivo"
  Então o sistema bloqueia a ação
  E exibe a mensagem de erro "Este MAC Address já está registrado em outro nó sensor"
```

---

## US02 - Visualização de Telemetria em Tempo Real (Dashboard)

**Como** analista de dados ou técnico de campo  
**Quero** visualizar os gráficos de telemetria dos sensores atualizados em tempo real  
**Para que** eu possa acompanhar as variações ambientais e operacionais sem recarregar a página manualmente  

### Cenários de Aceite (BDD)

```gherkin
Cenário: Atualização automática do gráfico de leitura
  Dado que estou visualizando o painel do sensor em "/forum/dispositivos/15/telemetria"
  Quando o sensor envia uma nova leitura de temperatura via protocolo MQTT ou HTTP
  Então o gráfico de linha adiona o novo ponto de dados com o valor e horário correspondentes
  E o indicador de "Última atualização" é alterado para "Agora mesmo"

Cenário: Perda de sinal do dispositivo (Timeout)
  Dado que o dispositivo "Sensor Estufa 01" está configurado para enviar dados a cada 30 segundos
  Quando o sistema não recebe nenhuma telemetria por um período superior a 3 minutos
  Então o indicador de status do dispositivo no painel muda automaticamente de "Online" para "Offline"
  E um alerta visual é exibido na lista de monitoramento
```

---

## US03 - Configuração de Limiares e Alertas de Limite Critico

**Como** gestor de monitoramento  
**Quero** configurar limiares de alerta (mínimo e máximo) para métricas de sensoriamento  
**Para que** a equipe seja notificada instantaneamente quando uma leitura sair da faixa operacional segura  

### Cenários de Aceite (BDD)

```gherkin
Cenário: Disparo de alerta por temperatura elevada
  Dado que o sensor "Sensor Estufa 01" possui o limiar máximo de temperatura configurado para 35.0 °C
  Quando o dispositivo envia uma leitura de telemetria igual a 37.5 °C
  Então o sistema registra uma ocorrência de alerta de nível "Crítico"
  E cria automaticamente um tópico de incidente no fórum central em "/forum/" informando o desvio
  E envia uma notificação push/e-mail para os responsáveis cadastrados

Cenário: Retorno da métrica para a faixa normal
  Dado que um dispositivo está em estado de "Alerta Ativo" por alta umidade
  Quando o sensor envia uma nova leitura dentro da faixa considerada segura (entre 40% e 60%)
  Então o status do alerta muda para "Normalizado"
  E o histórico de eventos é atualizado com o horário de resolução
```

---

## US04 - Discussão e Diagnóstico Colaborativo de Falhas no Fórum

**Como** técnico de manutenção  
**Quero** publicar ou abrir um tópico no fórum relacionado a um comportamento anômalo de um sensor  
**Para que** outros especialistas da comunidade/equipe possam ajudar no diagnóstico técnico  

### Cenários de Aceite (BDD)

```gherkin
Cenário: Abertura de tópico de diagnóstico vinculado a um sensor
  Dado que estou autenticado na página do fórum em "/forum/"
  Quando clico no botão "Novo Tópico de Diagnóstico"
  E seleciono o dispositivo associado "Sensor Pressão Tubulação B"
  E preencho o título "Oscilações anômalas na leitura de pressão"
  E descrevo o problema no campo de mensagem
  E clico em "Publicar Tópico"
  Então o tópico é criado em "/forum/" com uma tag vinculada ao ID do equipamento
  E os dados recentes de telemetria do sensor são anexados automaticamente à publicação

Cenário: Interação na resolução do problema
  Dado que existe um tópico de diagnóstico aberto em "/forum/topico/88"
  Quando um engenheiro publica uma resposta sugerindo "Verificar recalibração do sensor piezoelétrico"
  E o autor do tópico confirma a solução clicando em "Marcar como Solução Aceita"
  Então o tópico é marcado como "Diagnóstico Concluído"
```

---

## US05 - Exportação de Histórico de Dados de Sensoriamento

**Como** pesquisador ou auditor de dados  
**Quero** exportar o histórico de leituras telemétricas em formato CSV ou JSON por intervalo de datas  
**Para que** eu possa realizar análises preditivas externas e auditorias de conformidade  

### Cenários de Aceite (BDD)

```gherkin
Cenário: Exportação de arquivo CSV dentro do período selecionado
  Dado que estou no painel de exportação do sensor "/forum/dispositivos/15/exportar"
  Quando defino a data inicial como "2026-10-01" e a data final como "2026-10-10"
  E escolho o formato de saída "CSV"
  E clico em "Gerar Relatório"
  Então o download do arquivo "telemetria_sensor_15_20261001_20261010.csv" é iniciado
  E o conteúdo do arquivo contém os campos "timestamp", "sensor_id", "parametro", "valor" e "unidade"

Cenário: Solicitação de exportação sem registros no período
  Dado que seleciono um intervalo de datas em que o sensor esteve desligado/sem registros
  Quando clico em "Gerar Relatório"
  Então o sistema exibe o aviso "Nenhum dado de telemetria encontrado para o período selecionado"
  E nenhum arquivo é gerado para download
```

---

## US06 - Atuação Remota em Atuadores IoT (Comando de Saída)

**Como** operador de campo autorizador  
**Quero** enviar comandos remotos de atuação (ex: ligar exaustor, fechar válvula) através da plataforma  
**Para que** eu possa intervir em tempo real após analisar o status dos sensores  

### Cenários de Aceite (BDD)

```gherkin
Cenário: Envio de comando de atuação com confirmação
  Dado que estou autenticado com permissões de "Operador de Atuação"
  E estou visualizando o painel do atuador "Válvula de Solenóide 02"
  Quando aciono a chave seletora de estado para "LIGADO"
  E confirmo a ação no modal de segurança
  Então o sistema publica uma mensagem de comando no tópico MQTT correspondente
  E aguarda a mensagem de confirmação (ACK) do dispositivo
  E exibe o status "Comando executado com sucesso" quando o ACK é recebido

Cenário: Falha na resposta do atuador (Timeout de Comando)
  Dado que o operador enviou o comando "DESLIGAR" para a "Válvula de Solenóide 02"
  Quando o dispositivo não retorna a confirmação de recebimento (ACK) em até 10 segundos
  Então a interface exibe a mensagem de erro "Falha na comunicação com o atuador. Verifique a conexão do nó."
  E o estado visual do atuador permanece como "Inalterado/Erro"
```