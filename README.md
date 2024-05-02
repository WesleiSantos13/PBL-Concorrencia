# PBL-Concorrencia


DOCumentar a API

Comentar codigo e corrigir nome s de rotas e de funções

Corrijir as relações entre as funcoes de clientes e broker

exibir os topicos que ele está inscrito

O controle deve selecionar o dispositivo, para poder ligar

O cliente dá erro se executar sem o broker ligado ver isso aindaaaaa             OK

O cliente só pode receber mensagem de um sensor por vez

# ################################################# RELATÓRIO ##############################################################


### FUNCIONALIDADES:

# FILE: Brokers.py
Esse file é destinado para o broker-servidor em que ele possui uma API para atender as solicitações dos clientes.

# Introdução: 
    O servidor funciona da seguinte maneira, inicialmente a API é executada em uma threading e o broker irá ficar esperando mensagens em loop, essas abordagens foram utilizadas para a execução de ambas não se interrompessem. Para armazenar os dados foram utilizados listas e dicionários.

# Armazenamento de Dados:      
#   # Dicionário topic_subscriptions:
        Propósito: Este dicionário é usado para armazenar as inscrições dos clientes em cada tópico.
        Estrutura:   {"nome_do_topico": {"clients": {("endereco_ip", numero_da_porta): [mensagens_pendentes]},state": "estado_do_sensor"},...}
        
        Descrição: Cada chave representa o nome de um tópico, cujo o nome do topico será o nome do sensor.
       
        O valor correspondente é um dicionário que contém duas chaves:
           
           * "clients": Armazena os clientes inscritos no tópico, onde a chave é uma tupla contendo o endereço IP e o número da porta do cliente, e o valor é uma lista de mensagens pendentes para esse cliente.
          
           * "state": Indica o estado do sensor associado ao tópico (por exemplo, "Ligado" ou "Desligado").

#   # Dicionário endereco_disp:
        Propósito: Este dicionário é usado para armazenar as informações de endereço (endereço IP e porta) dos sensores.
        Estrutura: { "nome_do_topico": ("endereco_ip", numero_da_porta), ...}

        Descrição: Cada chave representa o nome de um tópico.
        O valor correspondente é uma tupla contendo o endereço IP e o número da porta do sensor associado ao tópico.

    Esses dicionários são essenciais para o funcionamento do servidor, pois mantêm o controle das inscrições dos clientes nos tópicos, as mensagens pendentes para cada cliente, o estado dos sensores e os endereços dos sensores. Isso permite que o servidor encaminhe mensagens aos clientes corretos, controle os sensores e mantenha um registro das inscrições e do estado dos dispositivos.

# Comunicações
    
# Comunicação HTTP:
    Protocolo: HTTP (Hypertext Transfer Protocol)
    Finalidade: A comunicação HTTP é usada para interações entre os clientes e o servidor web Flask. Os clientes enviam solicitações HTTP para o servidor através de endpoints específicos (por exemplo, /subscribe, /controlar_sensor) usando os métodos HTTP adequados (POST, GET, PUT). O servidor processa essas solicitações e retorna respostas HTTP correspondentes.
    Mecanismo: O framework flask é usado para criar uma aplicação no servidor web que escuta solicitações HTTP dos clientes. Os endpoints definidos na aplicação correspondem a diferentes ações que os clientes podem realizar. Por exemplo, inscrever-se em um tópico, controlar sensores, obter mensagens, etc.

   # As rotas da API são:
    
#   Inscrever-se em um Tópico:
    Endpoint: /subscribe
    Método HTTP: POST
    Payload JSON Esperado: {"topic": "nome_do_topico", "ip": "endereco_ip", "port": numero_da_porta}

    Descrição: Este endpoint permite que um cliente se inscreva em um tópico específico para receber mensagens do sensor fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.
    ----------------------------------------------------------------------

#   Desinscrever-se de um Tópico:
    Endpoint: /desinscrever
    Método HTTP: POST
    Payload JSON Esperado:{"topic": "nome_do_topico", "ip": "endereco_ip", "porta": numero_da_porta}
    
    Descrição: Este endpoint permite que um cliente se desinscreva de um tópico específico fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.
    ----------------------------------------------------------------------

#   Exibir Tópicos Disponíveis:
    Endpoint: /exibir_topicos
    Método HTTP: GET
    
    Descrição: Este endpoint retorna a lista de todos os tópicos disponíveis aos quais os clientes podem se inscrever.
    ----------------------------------------------------------------------

#   Controlar Sensor (Ligar/Desligar):
    Endpoint: /controlar_sensor
    Método HTTP: PUT
    Payload JSON Esperado: { "topic": "nome_do_topico", "acao": "ligar_ou_desligar"}

    Descrição: Este endpoint permite controlar o estado de um sensor em um determinado tópico. O sensor deve estar previamente inscrito no tópico. A ação pode ser "ligar" ou "desligar".
    ----------------------------------------------------------------------

#   Verificar Inscrição em um Tópico:
    Endpoint: /verificar_inscricao
    Método HTTP: GET
    Payload JSON Esperado: { "topic": "nome_do_topico", "ip": "endereco_ip", "porta": numero_da_porta}

    Descrição: Este endpoint verifica se um cliente está inscrito em um determinado tópico, fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.
    ----------------------------------------------------------------------

#   Obter Mensagens de um Tópico:
    Endpoint: /get_messages
    Método HTTP: GET
    Payload JSON Esperado: {"topic": "nome_do_topico",  "ip": "endereco_ip", "port": numero_da_porta}

    Descrição: Este endpoint permite que um cliente obtenha as mensagens pendentes de um determinado tópico, fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.
    ----------------------------------------------------------------------

#   Verificação de Atividade do Servidor:
    Endpoint: /verificacao
    Método HTTP: GET
    
    Descrição: Este endpoint retorna um status indicando se o servidor está ativo.
    ----------------------------------------------------------------------

# Comunicação UDP (User Datagram Protocol):
    Protocolo: UDP (User Datagram Protocol)
    Finalidade: A comunicação UDP é utilizada para receber mensagens do sensor.
    Mecanismo: Um socket UDP é criado no servidor e associado a um endereço IP e porta específicos. O servidor espera por mensagens UDP vindas do sensor nesse socket. Quando uma mensagem é recebida, ela é processada e encaminhada aos clientes inscritos no tópico correspondente. A função responsavel por receber as mensagens de chama (process_messages).

#    Função (process_messages)
        A função fica responsavel pelo processamento e encaminhamento de mensagens recebidas pelo servidor a partir do sensor. Ele interpreta o conteúdo das mensagens, atualiza o estado dos tópicos e dos sensores, e encaminha as mensagens pertinentes aos clientes inscritos. Essa função é importantissima para o funcionamento do sistema de comunicação entre o sensor e os clientes.

# Comunicação TCP (Transmission Control Protocol):
    Protocolo: TCP (Transmission Control Protocol)
    Finalidade: A comunicação TCP é usada para enviar comandos de ligar ou desligar para o sensor.
    Mecanismo: Quando um cliente envia um comando para ligar ou desligar um sensor, o servidor cria um novo socket TCP para se comunicar com o sensor associado ao tópico relevante. O servidor se conecta ao endereço IP e porta do sensor usando esse socket TCP e envia o comando apropriado. Isso permite controlar o estado do sensor de forma confiável. A rota que faz essa comunicação é a de controlar o sensor.(/controlar_sensor)
# ######################### ############ ############   ############        ###########  ##########################################


# FILE: dispositivo.py
    Esse file é destinado para o sensor/dispositivo que ira mandar mennsagem para o broker-servidor, e receber comandos de gerenciamento de ligar e desligar.

# Dicionário sensor:
    Propósito: Este dicionário é usado para armazenar informações sobre o sensor de temperatura, como seu nome, estado atual e temperatura simulada.
    Estrutura: sensor = {'Nome': 'Sensor de Temperatura','Estado': 'Desligado','Temperatura': 24}

    Descrição dos Campos:
    'Nome': O nome do sensor, que neste caso é "Sensor de Temperatura".
    'Estado': O estado atual do sensor, que pode ser "Ligado" ou "Desligado".
    'Temperatura': A temperatura simulada fornecida pelo sensor. Inicialmente, está definida como 24°C.

    Este dicionário é fundamental para acompanhar o estado e os dados do sensor de temperatura. Ele fornece uma estrutura organizada para armazenar e acessar essas informações durante a execução do programa.
    
    Por exemplo, durante a execução do programa, quando o sensor é ligado ou desligado, o estado no dicionário é atualizado. Da mesma forma, quando a temperatura simulada é alterada manualmente, o valor correspondente no dicionário é atualizado. Isso permite que o programa mantenha o controle do estado e dos dados do sensor em tempo real.

# Operações Básicas:
   
   * 1. Ligar o Sensor:
    Selecione a opção "1" para ligar o sensor de temperatura.
    O sensor começará a enviar dados de temperatura para o servidor.
   
   * 2. Desligar o Sensor:
    Selecione a opção "2" para desligar o sensor de temperatura.
    O sensor interromperá o envio de dados de temperatura para o servidor.
    
   * 3. Alterar Temperatura Manualmente:
    Selecione a opção "3" para alterar manualmente a temperatura simulada pelo sensor.
    Insira a nova temperatura desejada quando solicitado.
   
   * 4. Sair do Programa:
    Selecione a opção "4" para sair do programa e encerrar a execução.

# Comunicações

# Comunicação TCP:
O servidor TCP está disponível na porta 12349. Ele permite receber comandos de gerenciamento do servidor para ligar ou desligar o sensor.
    Função responsavel

# Comunicação UDP:
O servidor UDP está configurado para enviar mensagens de temperatura para o broker servidor. As mensagens são enviadas em formato JSON e devem conter o tópico, o conteúdo e a ação. O sensor envia dados de temperatura para o tópico inicialmente especificado.
    Função responsavel
# ################ ################## #################  ################  ########### ############# ############### ################

# File: Client.py
    Esse file é destinado ao cliente que faz requisições http para a Aplicação que está no broker servidor.

 #   Operações Básicas:
  * 1. Inscrever-se em um Tópico:
    Selecione a opção "1" para inscrever-se em um tópico.
    Uma lista de tópicos disponíveis será exibida com seus respectivos códigos.
    Digite o código do tópico desejado para se inscrever.
    
  * 2. Desinscrever-se de um Tópico:
    Selecione a opção "2" para desinscrever-se de um tópico.
    Uma lista de tópicos inscritos será exibida com seus respectivos códigos.
    Digite o código do tópico do qual deseja desinscrever-se.
    
  * 3. Ligar Sensor:
    Selecione a opção "3" para ligar o sensor de temperatura em um tópico inscrito.
    Será solicitado o código do tópico onde o sensor será ligado.
    Será verificado se o cliente está inscrito no topico para poder liga-lo.
    
  * 4. Desligar Sensor:
    Selecione a opção "4" para desligar o sensor de temperatura em um tópico inscrito.
    Será solicitado o código do tópico onde o sensor será desligado.
    Será verificado se o cliente está inscrito no topico para poder desliga-lo.
    
  * 5. Exibir Tópicos:
    Selecione a opção "5" para exibir a lista de tópicos disponíveis.
    
  * 6. Exibir Mensagem de um Tópico:
    Selecione a opção "6" para exibir a última mensagem recebida de um tópico inscrito.
    Será solicitado o código do tópico do qual deseja exibir a mensagem.
    Será verificado se o cliente está inscrito no topico para poder receber a mensagem.
  
  * 7. Exibir Mensagens Continuamente:
    Selecione a opção "7" para exibir as mensagens continuamente de um tópico inscrito.
    Será solicitado o código do tópico do qual deseja exibir as mensagens.
    Será verificado se o cliente está inscrito no topico para poder receber a mensagem.
    Pressione "Enter" para interromper a exibição contínua.
    
  * 8. Sair do Programa:
    Selecione a opção "8" para sair do programa e encerrar a execução.

# Comunicação HTTP:
    O cliente utiliza o protocolo HTTP (Hypertext Transfer Protocol) para se comunicar com o servidor broker. Ele envia solicitações HTTP para diferentes rotas do servidor e recebe respostas HTTP correspondentes.

#   Métodos HTTP Utilizados:
    POST: Utilizado para inscrever-se em um tópico, desinscrever-se de um tópico.
    GET: Utilizado para exibir os tópicos disponíveis, verificar a inscrição em um tópico, obter mensagens de um tópico e verificar o status do servidor.
    PUT: Utilizado solicitar a aplicação que ligue ou desligue o sensor.

# Observações Importantes:
    Certificar que o servidor broker esteja ativo e operacional para garantir o funcionamento adequado do cliente.
    Ao fazer a incrição ou desinscrição de um tópico, certifique-se de selecionar o código correto do tópico.
    O cliente utiliza comunicação HTTP para interagir com o servidor broker, então verificar a conectividade de rede adequada antes de usar o cliente.


# #### ORDEM DE INICIALIZAÇÃO Servidor -> Sensor -> Cliente
* É importante que o servidor seja executado primeiro
* Depois o sensor e o cliente podem ser executados sem problemas