# Histórias de Usuário - Plataforma de IoT e Sensoriamento

Este documento apresenta o levantamento das **User Stories** para o sistema de monitoramento IoT e os sensores, incluindo cenários de teste orientados a comportamento (BDD/Gherkin).

**Módulo principal:** [http://127.0.0.1:8000/forum/](http://127.0.0.1:8000/forum/) (Central de Discussões e Alertas da Comunidade IoT)

---

## US01 - Acesso e Início da Experiência do Simulador 

**Como** operador de fábrica ou usuário da plataforma  
**Quero** visualizar a página inicial do simulador com a apresentação dos conceitos e o botão de início  
**Para que** eu possa compreender o propósito do monitoramento IoT antes de iniciar a simulação  

### Cenários de Validação (BDD)

```gherkin
Cenário: Iniciar a experiência a partir da página inicial
  Dado que estou na página inicial do simulador IoT
  Quando visualizo o título da introdução e clico no botão "Começar experiência" 
  Então o sistema me redireciona para a tela da "Simulação 1 - Sem monitoramento" 
```

---

## US02 - Execução da Simulação Sem Monitoramento

**Como** usuário do simulador   
**Quero** iniciar a primeira simulação sem o monitoramento IoT ativo  
**Para que** eu possa observar como uma falha em uma máquina afeta em cadeia toda a linha de produção  

### Cenários de Validação (BDD)

```gherkin
Cenário: Induzir falha em linha de produção não monitorada
  Dado que estou na página da “Simulação 1” e o status do monitoramento é “INATIVO”
  Quando clico no botão “iniciar falha”
  Então o sistema executa a simulação mostrando a interrupção da máquina
  E o impacto acumulado na linha do tempo
  E exibe os indicadores dos impactos gerado
  E habilita o botão de “Continuar para a próxima simulação”
```

---

## US03 - Transição para o Cenário de Monitoramento

**Como** usuário do simulador  
**Quero** visualizar uma tela que demonstra os cenário do monitoramento com a BzuTech  
**Para que** eu entenda como a tecnologia IoT e os alertas antecipados previnem danos e prejuízos  

### Cenários de Validação (BDD)

```gherkin
Cenário: Avançar para simulação com monitoramento BZU
  Dado que concluiu a simulação 1 - sem monitoramento
  Quando clico em “Conhecer a simulação com a BZU”
  Então o sistema vai me direcionar ao ambiente da simulação 2 com sensores IoT ativos
```

---

## US04 - Execução da Simulação Com Monitoramento

**Como** gestor do sistema  
**Quero** receber alertas de anomalia em tempo real com opções de decisões  
**Para que** eu possa agir preventivamente antes que ocorra uma grave falha na máquina  

### Cenários de Validação (BDD)

```gherkin
Cenário:  Identificação de anomalia e acionamento de manutenção
  Dado que estou na página da “Simulação 2” e o status do monitoramento é “ATIVO”
  E o sensor detecta uma anomalia na Máquina 2
  Quando clico em “Iniciar simulação com BZU”
  E o painel exibe o alerta com as opções de tomada de decisão (“Ignorar alerta”, “Verificar dados”, “Acionar manutenção”)
  E seleciono a opção “Acionar manutenção”
  Então o sistema registra a intervenção preventiva e estabiliza a operação da máquina
  E exibe o impacto reduzido e o tempo/custo economizados
  E habilita o botão “Ver comparativo final”
```

---

## US05 - Inspeção de Telemetria e Linha do Tempo das Máquinas

**Como** usuário do simulador  
**Quero** selecionar uma máquina da linha de produção para visualizar seus dados de telemetria e o histórico da linha do tempo  
**Para que** eu possa acompanhar em tempo real as variações de temperatura, vibração e eficiência do equipamento  

### Cenários de Validação (BDD)

```gherkin
Cenário: Inspeção dos dados da máquina em tempo real
  Dado que estou visualizando uma simulação em andamento
  Quando clico sobre uma máquina na "Linha de Produção" (ex: "Máquina 02 — Processamento") 
  Então o painel de dados exibe os indicadores atualizados da máquina (Temperatura em °C, Vibração em mm/s, Eficiência e Uptime) 
  E a barra de progresso do indicador visual mostra se os valores estão dentro ou acima dos limites normais 
```

---

## US06 - Tomada de Decisão Preventiva na Simulação Monitorada

**Como** usuário ou operador do simulador  
**Quero** selecionar a ação de intervenção ("Acionar manutenção") ao receber um alerta de anomalia  
**Para que** eu possa evitar a parada total da linha de produção e reduzir os impactos operacionais  

### Cenários de Validação (BDD)

```gherkin
Cenário: Intervenção preventiva com sucesso na Simulação 2
  Dado que estou no ambiente da "Simulação 2" com o monitoramento BZU ativo 
  E o sistema exibe um alerta de anomalia na "Máquina 02" com opções de ação 
  Quando  clico na opção "Acionar manutenção" no painel de decisão 
  Então o sistema atualiza a linha do tempo informando que a equipe de manutenção foi acionada 
  E o status da máquina muda para "Protegida" ou "Operação normalizada" 
  E o painel exibe o resumo do impacto evitado (tempo de parada reduzido e custo economizado) 
```

---

## US07 - Visualização de Telemetria em Tempo Real (Dashboard)

**Como** analista de dados ou técnico de campo  
**Quero** visualizar os gráficos de telemetria dos sensores atualizados em tempo real  
**Para que** eu possa acompanhar as variações ambientais e operacionais sem recarregar a página manualmente  

### Cenários de Validação (BDD)

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

## US08- Atuação Remota em Atuadores IoT (Comando de Saída)

**Como** operador de campo autorizador  
**Quero** enviar comandos remotos de atuação (ex: ligar exaustor, fechar válvula) através da plataforma  
**Para que** eu possa intervir em tempo real após analisar o status dos sensores  

### Cenários de Validação (BDD)

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

