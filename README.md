# PBL-Concorrencia

#                ##### ####                  COMO USAR O PROGRAMA   #############  ##########   ########     ###############
#   Configuração Inicial
    
    O sistema tem como código fonte a linguagem python, por isso é necesário que o ambiente que irá rodar o programa tenha o python instalado.
        Link para baixar o python nos diferentes sistemas operacionais: https://www.python.org/downloads/
        A versão utilizada foi a 3.12
    
    Depois é necessário instalar a API do flask, usando o comando pip do python no prompt de comando:
        pip install flask (Apenas o servidor necessita do flask)
    
    E instalar a biblioteca requests, que é responsável pelas solicitacões dos clientes via http. Instale  usando o prompt de comando com:
        pip install requests (Apenas os clientes/aplicações necessitam da requests)

#    Utilização do Programa (Execução) #### #####

# Servidor(server.py)
    O servidor é responsável por gerenciar as conexões entre os clientes e os sensores.
    Iniciar o Servidor: Execute o arquivo server.py utilizando Python. Isso iniciará o servidor e estará pronto para aceitar conexões de clientes e sensores. 
#       É ESSENCIAL QUE O SERVIDOR ESTEJA EM EXECUÇÃO PARA O FUNCIONAMENTO CORRETO DO PROGRAMA*****


# Sensor(device.py)
O sensor é responsável por enviar informações de temperatura para o servidor.

Ativação do Sensor: Execute o arquivo device.py utilizando Python. Isso iniciará o sensor e irá aparecer o menu para enviar dados paara o servidor.
Desativação do Sensor: Basta fechar a janela ou interromper a execução do programa para desativar o sensor.
 # Funcionalidades do sensor

   * 0. Criar um tópico para enviar mensagem:
    Selecione a opção 0 para Criar um tópico para enviar mensagem, para os clientes.
    O sensor cria um tópico no servidor que ira armazenar as inscrições dos clientes.

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



# Cliente/Aplicação(client.py)
  O cliente é responsável por interagir com o servidor, permitindo que os usuários inscrevam-se em tópicos, recebam mensagens e controlem os sensores.
  Iniciar o Cliente: Execute o arquivo client.py utilizando Python. Isso iniciará o cliente e exibirá um menu interativo com as opções disponíveis.
  # Funcionalidades do cliente:
    1. Inscrever-se em um tópico. 
        Nessa opção o cliente se registra em topico para receber mensagem do sensor, ele só pode se inscrever em um tópico se o sensor registrar um topico no servidor para encaminhar as mensagens.
        
    2. Desinscrever-se de um tópico.
        Nessa opção o cliente apaga seu registro do topico pelo qual o sensor envia mensagens, então o cliente para de receber dados do sensor que mandava mensagens através do tópico.

    3. Ligar um sensor.
        Só depois de inscrito no topico correspondente ao sensor, o cliente pode pedir para o servidor ligar o sensor 
        Nessa funcionalidade o cliente pode ligar o sensor, solicitando ao servidor para ligar
        As mensagens enviadas ficarão sendo armazenadas na lista de mensagens pendentes de TODOS OS CLIENTES que estão inscritos no tópico, até ele consultar as mensagens coma opção 6 ou 7.
        
    4. Desligar um sensor.
        Só depois de inscrito no topico correspondente ao sensor, o cliente pode pedir para o servidor desligar o sensor
        Nessa funcionalidade o cliente pode desligar o sensor, solicitando ao servidor para desligar
        As mensagens enviadas deixarão de ser armazenadas na lista de mensagens pendentes do cliente e dos demais que estão no inscritos no tópico.
   
    5. Exibir tópicos disponíveis.
        Exibe os topicos criados pelos sensores

    6. Exibir mensagens de um tópico.
        Nessa funcionalidade o cliente pode receber as mensagens que estão pendentes em sua lista de mensagens pendentes, tudo isso por topico
        Se o sensor responsavel por mandar mensagens nesse tópico estiver desligado, o cliente não pode exibir mensagens.
    7. Exibir mensagens de um tópico continuamente.
        Essa opção exibe as mensagens pendentes continuamente
    8. Sair.


# ################################################# RELATÓRIO ##############################################################


### FUNCIONALIDADES:

# FILE: server.py
Esse file é destinado para o broker-servidor em que ele possui uma API para atender as solicitações dos clientes.

# Introdução: 
    O servidor funciona da seguinte maneira, inicialmente a API é executada em uma threading e o servidor irá ficar esperando mensagens em loop, essas abordagens foram utilizadas para a execução de ambas não se interrompessem. Para armazenar os dados foram utilizados listas e dicionários.

# Armazenamento de Dados:      
#   # Dicionário topic_subscriptions:
        Propósito: Este dicionário é usado para armazenar as inscrições dos clientes em cada tópico, mensagens pendentes e o estado do sensor.
        Estrutura:   {"nome_do_topico": {"clients": {("endereco_ip", numero_da_porta): [mensagens_pendentes]},state": "estado_do_sensor"},...}
                                
        Descrição: Cada chave representa o nome de um tópico, cujo o nome do topico será o nome do sensor.
       
        O valor correspondente é um dicionário que contém duas chaves:
           
           * "clients": Armazena os clientes inscritos no tópico, onde a chave é uma tupla contendo o endereço IP e o número da porta do cliente, e o valor é uma lista de mensagens pendentes para esse cliente.
          
           * "state": Indica o estado do sensor associado ao tópico (por exemplo, "Ligado" ou "Desligado").

#   # Dicionário endereco_disp:
        Propósito: Este dicionário é usado para armazenar as informações de endereço (endereço IP e porta) dos sensores.
        Estrutura: { "nome_do_topico": ("endereco_ip", numero_da_porta), ...}

        Descrição: Cada chave representa o nome de um tópico, cujo o nome do topico será o nome do sensor.
        O valor correspondente é uma tupla contendo o endereço IP e o número da porta do sensor associado ao tópico.

    Esses dicionários são essenciais para o funcionamento do servidor, pois mantêm o controle das inscrições dos clientes nos tópicos, as mensagens pendentes para cada cliente, o estado dos sensores e os endereços dos sensores. Isso permite que o servidor encaminhe mensagens aos clientes corretos, controle os sensores e mantenha um registro das inscrições e do estado dos dispositivos.

# Comunicações do Servidor
    
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
    Endpoint: /unsubscribe
    Método HTTP: POST
    Payload JSON Esperado:{"topic": "nome_do_topico", "ip": "endereco_ip", "port": numero_da_porta}
    
    Descrição: Este endpoint permite que um cliente se desinscreva de um tópico específico fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.
    ----------------------------------------------------------------------

#   Exibir Tópicos Disponíveis:
    Endpoint: /display_topics
    Método HTTP: GET
    
    Descrição: Este endpoint retorna a lista de todos os tópicos disponíveis aos quais os clientes podem se inscrever.
    ----------------------------------------------------------------------

#   Controlar Sensor (Ligar/Desligar):
    Endpoint: /control_device
    Método HTTP: PUT
    Payload JSON Esperado: { "topic": "nome_do_topico", "action": "ligar_ou_desligar", "ip": "endereco_ip", "port": numero_da_porta}

    Descrição: Este endpoint permite controlar o estado de um sensor de um determinado tópico. O sensor deve estar previamente inscrito no tópico. A ação pode ser "ligar" ou "desligar", além disso essa rota verifica se o cliente que quer controlar o sensor está inscrito no tópico, pois caso contrário ele não poderá controlar o sensor.
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
    Mecanismo: Um socket UDP é criado no servidor e associado a um endereço IP e porta específicos. O servidor espera por mensagens UDP vindas do sensor nesse socket. Quando uma mensagem é recebida, ela é processada e encaminhada para a lista de mensagens pendentes de cada cliente inscrito no tópico correspondente. A função responsavel por receber as mensagens de chama (process_messages).

#    Função (process_messages)
        A função fica responsavel pelo processamento e encaminhamento de mensagens recebidas pelo servidor a partir do sensor. Ele interpreta o conteúdo das mensagens, atualiza o estado dos tópicos e dos sensores, e encaminha as mensagens pertinentes aos clientes inscritos. Essa função é importantissima para o funcionamento do sistema de comunicação entre o sensor e os clientes.

# Comunicação TCP (Transmission Control Protocol):
    Protocolo: TCP (Transmission Control Protocol)
    Finalidade: A comunicação TCP é usada para enviar comandos de ligar, desligar ou alterar a temperatura do sensor.
    Mecanismo: Quando um cliente envia um comando para ligar desligar, ou alterar dados do sensor, o servidor cria um novo socket TCP para se comunicar com o sensor associado ao tópico relevante. O servidor se conecta ao endereço IP e porta do sensor usando esse socket TCP e envia o comando apropriado. Isso permite controlar o estado e os dados do sensor de forma confiável. A rota que faz essa comunicação é a de controlar o sensor.(/control_device)
# ######################### ############ ############   ############        ###########  ##########################################


# FILE: device.py
    Esse file é destinado para o sensor/dispositivo que ira mandar mennsagem de temperatura para o broker-servidor, e receber comandos de gerenciamento de ligar e desligar e alterar de temperatura.
# Armazenamento de Dados:
#   Dicionário sensor:
    Propósito: Este dicionário é usado para armazenar informações sobre o sensor de temperatura, como seu nome, estado atual e temperatura simulada.
    Estrutura: device = {'Nome': 'Sensor de Temperatura', 'Estado': 'Desligado', 'Temperatura': 24, 'Registrado': False}

    Descrição dos Campos:
    'Nome': O nome do sensor, que neste caso é "Sensor de Temperatura".
    'Estado': O estado atual do sensor, que pode ser "Ligado" ou "Desligado".
    'Temperatura': A temperatura simulada fornecida pelo sensor. Inicialmente, está definida como 24°C.
    'Registrado': serve para saber se o sensor criou um tópico para envio de mensagens (True ou False)

    Este dicionário é fundamental para acompanhar o estado e os dados do sensor de temperatura. Ele fornece uma estrutura para armazenar e acessar essas informações durante a execução do programa.
    
    Por exemplo, durante a execução do programa, quando o sensor é ligado ou desligado, o estado no dicionário é atualizado. Da mesma forma, quando a temperatura simulada é alterada manualmente, o valor correspondente no dicionário é atualizado. Isso permite que o programa mantenha o controle do estado e dos dados do sensor em tempo real.

# Comunicações do sensor de temperatura

  # Comunicação TCP:
    O socket TCP está disponível na porta 12349. Ele permite receber comandos de gerenciamento do servidor para ligar, desligar ou alterar a temperatura do sensor, essa conecção só aceita um dispositivo gerenciador de cada vez.


 # Comunicação UDP:
   O socket UDP está configurado para enviar mensagens de temperatura para o servidor. As mensagens são enviadas em formato JSON e devem conter o tópico, o conteúdo e a ação. O sensor envia dados de temperatura para o tópico inicialmente especificado. a função resposável por isso é chamada send_message e reading_device.
    
# Funções:
 #  send_message(topic, content, action):
    Esta função é responsável por enviar mensagens para o servidor UDP. Ela recebe o tópico da mensagem, o conteúdo da mensagem e a ação associada.

 # reading_device():
    Esta função simula a leitura de dados do sensor. Ela é executada em um loop enquanto o estado do dispositivo é 'Ligado'. A temperatura é atualizada periodicamente e enviada para o servidor UDP.

 # handle_tcp_connection(connection):
    Esta função lida com as conexões TCP recebidas pelo servidor. Ela recebe uma conexão como entrada e fica em um loop para receber dados do cliente. Dependendo do comando recebido, ela pode ligar, desligar e alterar a temperatura do sensor.

 # on_device():
    Esta função é responsável por ligar o sensor. Se o estado do dispositivo for 'Desligado', ele é alterado para 'Ligado', e uma nova thread é iniciada para simular a leitura do sensor.

 # off_device():
    Esta função é responsável por desligar o sensor. Se o estado do dispositivo for 'Ligado', ele é alterado para 'Desligado', e uma mensagem de desligamento é enviada para o servidor UDP, para atualizar o dicionário de registro do servidor(topic_subscriptions).

 # change_temperature():
    Esta função permite alterar manualmente a temperatura do sensor. Ela solicita uma nova temperatura ao usuário e a atualiza no dicionário de configuração do dispositivo.

 # create_topic(topic):
    Esta função cria um tópico para enviar mensagens de temperatura. Ela envia uma mensagem para o servidor UDP com a ação de inscrição ('subscribe'), o nome do tópico e as informações de endereço IP e porta do servidor TCP para poder receber comando de gerenciamento via TCP.

# tcp_server_thread():
    Esta função é executada em uma thread separada e lida com as conexões TCP recebidas pelo servidor. Quando uma conexão é aceita, uma nova thread é iniciada para lidar com ela.


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