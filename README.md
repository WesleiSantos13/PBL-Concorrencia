# PBL-Concorrência

_# COMO USAR O PROGRAMA_
   
Configuração Inicial
    
O sistema tem como código fonte a linguagem python, por isso é necessário que o ambiente que irá rodar o programa tenha o python instalado.
Link para baixar o python nos diferentes sistemas operacionais: https://www.python.org/downloads/ .
A versão utilizada foi a 3.12.
    
Depois é necessário instalar a API do flask, usando o comando pip do python no prompt de comando (Apenas o broker necessita do flask):
    
    pip install flask 
    
E instalar a biblioteca requests, que é responsável pelas solicitações dos clientes via http (Apenas os clientes/aplicações necessitam das requests). Instale usando o prompt de comando com:

    pip install requests 

__Utilização do Programa (Execução)__

**Broker(server.py)**  
 O broker é responsável por gerenciar as conexões entre os clientes e os sensores.  
 Iniciar o Broker: Execute o arquivo server.py utilizando Python. Isso iniciará o servidor e estará pronto para aceitar conexões de clientes e sensores. 
    
**Sensor(device.py)**  
O sensor é responsável por enviar informações de temperatura para o broker.  
Iniciar Sensor: Execute o arquivo device.py utilizando Python toda vez que quiser um novo sensor de temperatura. Isso iniciará o sensor e irá aparecer o menu para enviar dados para o broker.

* Funcionalidades do sensor:

   * 1. Criar um tópico para enviar mensagem:  
    Selecione a opção 0 para Criar um tópico para enviar mensagem, para os clientes.  
    O sensor cria um tópico no broker que irá armazenar as inscrições dos clientes.  

   * 2. Ligar o Sensor:  
    Selecione a opção "1" para ligar o sensor de temperatura.    
    O sensor começará a enviar dados de temperatura para o broker.  
   
   * 3. Desligar o Sensor:  
    Selecione a opção "2" para desligar o sensor de temperatura.    
    O sensor interrompe o envio de dados de temperatura para o broker.  
    
   * 4. Alterar Temperatura Manualmente:  
    Selecione a opção "3" para alterar manualmente a temperatura simulada pelo sensor.    
    Insira a nova temperatura desejada quando solicitado.
   
   * 5. Sair do Programa:  
    Selecione a opção "4" para sair do programa e encerrar a execução.



__Cliente/Aplicação(client.py)__  
O cliente é responsável por interagir com o broker, permitindo que os usuários inscrevam-se em tópicos, recebam mensagens e controlem os sensores.  
Iniciar o Cliente: Execute o arquivo client.py utilizando Python. Isso iniciará o cliente e exibirá um menu interativo com as opções disponíveis.

* Funcionalidades do cliente:

  * 1. Inscrever-se em um tópico.   
   Nessa opção o cliente se registra em topico para receber mensagem do sensor, ele só pode se inscrever em um tópico se o sensor registrar um topico no servidor para encaminhar as mensagens.
        
  * 2. Desinscrever-se de um tópico.  
   Nessa opção o cliente apaga seu registro do topico pelo qual o sensor envia mensagens, então o cliente para de receber dados do sensor, que mandava mensagens através do tópico.

   * 3. Ligar um sensor.  
    Nessa funcionalidade o cliente pode ligar o sensor, solicitando ao broker para ligar, selecionando a opção correspondente ao sensor.  
    Só depois de inscrito no topico correspondente ao sensor, o cliente pode pedir para o broker ligar o sensor.  
    As mensagens enviadas ficarão sendo armazenadas na lista de mensagens pendentes de TODOS OS CLIENTES que estão inscritos no tópico, até ele consultar as mensagens com a opção 6 ou 7.
   
    * 4. Alterar o dado de um sensor.  
     Nessa funcionalidade o cliente pode alterar a temperatura do sensor, solicitando ao broker para alterar, selecionando o tópico correspondente ao sensor.  
     Só depois de inscrito no topico correspondente ao sensor, o cliente pode alterar o dado do sensor.

    * 5. Desligar um sensor.  
     Nessa funcionalidade o cliente pode desligar o sensor, solicitando ao broker para desligar.  
     Só depois de inscrito no topico correspondente ao sensor, o cliente pode pedir para o broker desligar o sensor.  
     As mensagens enviadas deixarão de ser armazenadas na lista de mensagens pendentes do cliente e dos demais que estão no inscritos no tópico.
   
    * 6. Exibir tópicos disponíveis.  
     Exibe os topicos criados pelos sensores

    * 7. Exibir mensagens de um tópico.  
     Nessa funcionalidade o cliente pode receber as mensagens que estão pendentes em sua lista de mensagens pendentes, tudo isso por tópico.  
     Se o sensor responsável por mandar mensagens nesse tópico estiver desligado, o cliente não pode exibir mensagens.
   
    * 8. Exibir mensagens de um tópico continuamente.  
     Essa opção exibe as mensagens pendentes continuamente, caso o sensor esteja ligado.
   
    * 9. Sair.  


__Execução dos containers:__  
* Comandos para executar o sistema com o Docker:
 
Para carregar as imagens do DockerHub:  
 
     docker pull wesleisantoss/server:latest  
     docker pull wesleisantoss/client:latest  
     docker pull wesleisantoss/device:latest  


Para executar em qualquer máquina os containers:  

      docker run  --network=host -it wesleisantoss/server  
      docker run --network=host -it -e IP_SERVER=172.16.103.1 wesleisantoss/client  
      docker run --network=host -it -e IP_SERVER=172.16.103.1 wesleisantoss/device  

Inicialmente execute o broker (wesleisantoss/server), depois coloque o ip onde está executando o broker no cliente (wesleisantoss/client) e no dispositivo (wesleisantoss/device) e execute.



-------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------RELATÓRIO--------------------------------------

__INTRODUÇÃO:__  
    O projeto em questão consiste no desenvolvimento de um sistema de monitoramento de temperatura, que utiliza uma arquitetura de comunicação baseada em um modelo de publish-subscribe (publicação e inscrição). O sistema é composto por três componentes principais: o sensor de temperatura, os clientes (ou dispositivos consumidores) e o servidor central (broker) responsável por gerenciar a comunicação entre eles.

* O sensor de temperatura é responsável por coletar dados de temperatura e enviar essas informações periodicamente para o servidor central. Ele também pode receber comandos de controle remoto, como ligar, desligar e alterar manualmente os dados de temperatura.  
* Os clientes, por sua vez, podem se inscrever em tópicos específicos no servidor central para receber atualizações de temperatura do sensor. Eles também têm a capacidade de enviar comandos para o sensor, como ligar, desligar e solicitar informações sobre as mensagens mais recentes recebidas.  
* O servidor central atua como um intermediário entre os sensores e os clientes, gerenciando as inscrições nos tópicos, encaminhando mensagens entre os participantes e coordenando as operações de controle do sensor. Ele é responsável por manter um registro dos tópicos disponíveis, as inscrições dos clientes e as mensagens pendentes para entrega.

* A comunicação entre os componentes do sistema é realizada principalmente por meio de sockets UDP (User Datagram Protocol) para transmissão eficiente de dados em tempo real, sockets TCP (Transmission Control Protocol) para comunicação de controle mais confiável, e requisições HTTP (Hypertext Transfer Protocol) usada para interações entre os clientes e o servidor web Flask.
    

__FUNCIONALIDADES:__  

__FILE:__ _server.py_  
Esse file é destinado para o broker-servidor em que ele possui uma API para atender as solicitações dos clientes.  
O servidor funciona da seguinte maneira, inicialmente a API é executada em uma threading e o servidor irá ficar esperando mensagens em loop, essas abordagens foram utilizadas para a execução de ambas não se interrompessem. Para armazenar os dados foram utilizados listas e dicionários.

__Armazenamento de Dados:__     
* Dicionário "topic_subscriptions":  
  * Propósito: Este dicionário é usado para armazenar as inscrições dos clientes em cada tópico, mensagens pendentes e o estado do sensor.  
  * Estrutura:   {"nome_do_topico": {"clients": {("endereco_ip", numero_da_porta): [mensagens_pendentes]},state": "estado_do_sensor"},...}                       
  * Descrição: Cada chave representa o nome de um tópico, cujo o nome do topico será o nome do sensor.   
  * O valor correspondente é um dicionário que contém duas chaves:  
    * "clients": Armazena os clientes inscritos no tópico, onde a chave é uma tupla contendo o endereço IP e o número da porta do cliente, e o valor é uma lista de mensagens pendentes para esse cliente.
    * "state": Indica o estado do sensor associado ao tópico (por exemplo, "Ligado" ou "Desligado").

* Dicionário "endereco_disp":
  * Propósito: Este dicionário é usado para armazenar as informações de endereço (endereço IP e porta) dos sensores.  
  * Estrutura: { "nome_do_topico": ("endereco_ip", numero_da_porta), ...}  
  * Descrição: Cada chave representa o nome de um tópico, cujo o nome do topico será o nome do sensor.  
  * O valor correspondente é uma tupla contendo o endereço IP e o número da porta do sensor associado ao tópico.  

Esses dicionários são essenciais para o funcionamento do servidor, pois mantêm o controle das inscrições dos clientes nos tópicos, as mensagens pendentes para cada cliente, o estado dos sensores e os endereços dos sensores. Isso permite que o servidor encaminhe mensagens aos clientes corretos, controle os sensores e mantenha um registro das inscrições e do estado dos dispositivos.

__Comunicações do Broker:__
    
* __Comunicação HTTP:__  
__Protocolo:__ HTTP (Hypertext Transfer Protocol)  
__Finalidade:__ A comunicação HTTP é usada para interações entre os clientes e o servidor web Flask. Os clientes enviam solicitações HTTP para o servidor através de endpoints específicos (por exemplo, /subscribe, /controlar_sensor) usando os métodos HTTP adequados (POST, GET, PUT). O servidor processa essas solicitações e retorna as respostas HTTP correspondentes.  
__Mecanismo__: O framework flask é usado para criar uma aplicação no servidor web que escuta solicitações HTTP dos clientes. Os endpoints definidos na aplicação correspondem a diferentes ações que os clientes podem realizar. Por exemplo, inscrever-se em um tópico, controlar sensores, obter mensagens, etc.

  * As rotas da API são:   
    Inscrever-se em um Tópico:
     *   Endpoint: /subscribe
     *   Método HTTP: POST  
     *   Payload JSON Esperado: {"topic": "nome_do_topico", "ip": "endereco_ip", "port": numero_da_porta}
     *  scrição: Este endpoint permite que um cliente se inscreva em um tópico específico para receber mensagens do sensor fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.
 
    Desinscrever-se de um Tópico:  
     * Endpoint: /unsubscribe  
     * Método HTTP: POST  
     * Payload JSON Esperado:{"topic": "nome_do_topico", "ip": "endereco_ip", "port": numero_da_porta}  
     * Descrição: Este endpoint permite que um cliente se desinscreva de um tópico específico fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.  
    

    Exibir Tópicos Disponíveis:  
    *    Endpoint: /display_topics  
    *    Método HTTP: GET  
    *    Descrição: Este endpoint retorna a lista de todos os tópicos disponíveis aos quais os clientes podem se inscrever.  
    

    Controlar Sensor (Ligar/Desligar/Alterar temperatura):
    *   Endpoint: /control_device  
    *   Método HTTP: PUT  
    *   Payload JSON Esperado: { "topic": "nome_do_topico", "action": "ligar_ou_desligar_ou_alterar", "ip": "endereco_ip", "port": numero_da_porta}  
    *   Descrição: Este endpoint permite controlar o estado e temperatura de um sensor de um determinado tópico. O sensor deve estar previamente inscrito no tópico. A ação pode ser "ligar", "desligar" ou "Alterar", além disso essa rota verifica se o cliente que quer controlar o sensor está inscrito no tópico, pois caso contrário ele não poderá controlar o sensor.
    

    Obter Mensagens de um Tópico:
    *   Endpoint: /get_messages  
    *   Método HTTP: GET  
    *   Payload JSON Esperado: {"topic": "nome_do_topico",  "ip": "endereco_ip", "port": numero_da_porta}  
    *   Descrição: Este endpoint permite que um cliente obtenha as mensagens pendentes de um determinado tópico, fornecendo o nome do tópico, o endereço IP do cliente e o número da porta.


* __Comunicação UDP:__  
    __Protocolo:__ UDP (User Datagram Protocol)  
    __Finalidade:__ A comunicação UDP é utilizada para receber mensagens do sensor.  
    __Mecanismo:__ Um socket UDP é criado no servidor e associado a um endereço IP e porta específicos. O servidor espera por mensagens UDP vindas do sensor nesse socket. Quando uma mensagem é recebida, ela é processada e encaminhada para a lista de mensagens pendentes de cada cliente inscrito no tópico correspondente. A função responsável por receber as mensagens de chama (process_messages).

  * Função (process_messages)
        A função fica responsável pelo processamento e encaminhamento de mensagens recebidas pelo servidor a partir do sensor. Ele interpreta o conteúdo das mensagens, atualiza o estado dos tópicos e dos sensores, e encaminha as mensagens pertinentes aos clientes inscritos. Essa função é importantíssima para o funcionamento do sistema de comunicação entre o sensor e os clientes.

* __Comunicação TCP:__  
    __Protocolo:__ TCP (Transmission Control Protocol)  
    __Finalidade:__ A comunicação TCP é usada para enviar comandos de ligar, desligar ou alterar a temperatura do sensor.  
    __Mecanismo:__ Quando um cliente envia um comando para ligar desligar, ou alterar dados do sensor, o servidor cria um novo socket TCP para se comunicar com o sensor associado ao tópico relevante. O servidor se conecta ao endereço IP e porta do sensor usando esse socket TCP e envia o comando apropriado. Isso permite controlar o estado e os dados do sensor de forma confiável. A rota que faz essa comunicação é a de controlar o sensor (/control_device).



__FILE:__ _device.py_  
    Esse file é destinado para o sensor/dispositivo que irá mandar mensagem de temperatura para o broker, e receber comandos de gerenciamento de ligar e desligar e alterar de temperatura.  
    
__Armazenamento de Dados:__
* Dicionário "device":
  *   Propósito: Este dicionário é usado para armazenar informações sobre o sensor de temperatura, como seu nome, estado atual e temperatura simulada.
  *   Estrutura: device = {'Nome': 'Sensor_temp_4444', 'Estado': 'Desligado', 'Temperatura': 24, 'Registrado': False}
  *   Descrição dos Campos:
      *   'Nome': O nome do sensor, que neste caso é "Sensor_temp_4444".
      *   'Estado': O estado atual do sensor, que pode ser "Ligado" ou "Desligado".
      *   'Temperatura': A temperatura simulada fornecida pelo sensor. Inicialmente, está definida como 24°C.
      *   'Registrado': serve para saber se o sensor criou um tópico para envio de mensagens (True ou False)

Este dicionário é fundamental para acompanhar o estado e os dados do sensor de temperatura. Ele fornece uma estrutura para armazenar e acessar essas informações durante a execução do programa.
    
Por exemplo, durante a execução do programa, quando o sensor é ligado ou desligado, o estado no dicionário é atualizado. Da mesma forma, quando a temperatura simulada é alterada manualmente, o valor correspondente no dicionário é atualizado. Isso permite que o programa mantenha o controle do estado e dos dados do sensor em tempo real.

__Comunicações do sensor de temperatura:__

* __Comunicação TCP:__
    O socket TCP estará disponível em uma porta aleatória criada selecionada pelo sistema. Ele permite receber comandos de gerenciamento do servidor para ligar, desligar ou alterar a temperatura do sensor, essa conexão só aceita um dispositivo gerenciador de cada vez.


* __Comunicação UDP:__
   O socket UDP está configurado para enviar mensagens de temperatura para o servidor. As mensagens são enviadas em formato JSON e devem conter o tópico, o conteúdo e a ação. O sensor envia dados de temperatura para o tópico inicialmente especificado. A função responsável por isso é chamada send_message e reading_device.
    
*  Funções:
    *  send_message(topic, content, action):  
    Esta função é responsável por enviar mensagens para o servidor UDP. Ela recebe o tópico da mensagem, o conteúdo da mensagem e a ação associada.

    * reading_device():  
    Esta função simula a leitura de dados do sensor. Ela é executada em um loop enquanto o estado do dispositivo é 'Ligado'. A temperatura é atualizada periodicamente e enviada para o servidor UDP.

    * process_tcp_connection(connection):  
    Esta função lida com as conexões TCP recebidas pelo servidor. Ela recebe uma conexão como entrada e fica em um loop para receber dados do cliente. Dependendo do comando recebido, ela pode ligar, desligar e alterar a temperatura do sensor.

    * on_device():  
    Esta função é responsável por ligar o sensor. Se o estado do dispositivo for 'Desligado', ele é alterado para 'Ligado', e uma nova thread é iniciada para simular a leitura do sensor.

    * off_device():  
    Esta função é responsável por desligar o sensor. Se o estado do dispositivo for 'Ligado', ele é alterado para 'Desligado', e uma mensagem de desligamento é enviada para o servidor UDP, para atualizar o dicionário de registro do servidor(topic_subscriptions).

    * change_temperature():  
    Esta função permite alterar manualmente a temperatura do sensor. Ela solicita uma nova temperatura e a atualiza no dicionário de configuração do dispositivo ("device").

    * create_topic(topic):  
    Esta função cria um tópico para enviar mensagens de temperatura. Ela envia uma mensagem para o servidor UDP com a ação de inscrição ('subscribe'), o nome do tópico e as informações de endereço IP e porta do servidor TCP para poder receber comandos de gerenciamento.

    * tcp_server_thread():  
    Esta função é executada em uma thread separada e lida com as conexões TCP recebidas pelo servidor. Quando uma conexão é aceita, uma nova thread é iniciada para lidar com ela.




__File:__ _client.py_  
    Esse file é destinado ao cliente que faz requisições http para a API que está no broker servidor.

* Funções:

   *    subscribe_to_topic(topic):  
    Descrição: Esta função permite que o cliente se inscreva em um tópico específico no broker, usando a rota /subscribe da API.  
   *   unsubscribe_to_topic(topic):  
    Descrição: Esta função permite que o cliente cancele a inscrição em um tópico específico no broker, usando a rota /unsubscribe da API.  
   *   exibir_topicos():  
    Descrição: Esta função solicita ao broker uma lista dos tópicos disponíveis e os exibe, usando a rota /display_topics da API.  
   *   on_device(topic):  
    Descrição: Esta função envia um comando para ligar o sensor associado ao tópico fornecido ao broker, usando a rota /control_device.  
   *   change_data(topic, change):  
    Descrição: Esta função envia um comando para alterar os dados do sensor associado ao tópico fornecido ao broker, usando a rota /control_device.  
   *   off_device(topic):  
    Descrição: Esta função envia um comando para desligar o sensor associado ao tópico fornecido ao broker, usando a rota /control_device.  
   *   get_messages_from_topic(topic):  
    Descrição: Esta função solicita ao broker as últimas mensagens recebidas em um tópico específico e as exibe, usando a rota /get_messages.  
   *  thread_get_messages(event, topic):  
    Descrição: Esta função é executada em uma thread separada para receber continuamente as mensagens de um tópico específico e exibi-las, usando a rota /get_messages com várias chamadas dentro de um loop.  

   * Comunicação HTTP:  
    O cliente utiliza o protocolo HTTP (Hypertext Transfer Protocol) para se comunicar com o servidor broker. Ele envia solicitações HTTP para diferentes rotas do servidor e recebe respostas HTTP correspondentes.

   *   Métodos HTTP Utilizados:
    POST: Utilizado para inscrever-se em um tópico, desinscrever-se de um tópico.
    GET: Utilizado para exibir os tópicos disponíveis, obter mensagens de um tópico.
    PUT: Utilizado para solicitar a aplicação que ligue, desligue o sensor e também serve para alterar os dados de temperatura que estão sendo enviados.

   * Observações Importantes:
  Certificar que o servidor broker esteja ativo e operacional para garantir o funcionamento adequado do cliente.

    O cliente utiliza comunicação HTTP para interagir com o servidor broker, então verificar a conectividade de rede adequada antes de executar o cliente.


* ORDEM DE INICIALIZAÇÃO (1°) Broker -> (2° ou 3°) Sensor <-> (2° ou 3°) Cliente.
   *   É importante que o broker seja executado primeiro.
   *   Depois o sensor ou cliente podem ser executados sem problemas.


__CONCLUSÃO:__  
  - O projeto demonstra com sucesso a criação de um sistema de monitoramento de temperatura usando a arquitetura publish-subscribe, mostrando-se flexível, escalável e eficiente. Utilizando diferentes protocolos de comunicação e possibilitando o controle remoto dos sensores, o sistema oferece uma solução prática e interessante para o monitoramento em tempo real. Com melhorias adicionais em segurança, robustez e interface de usuário, o sistema pode ser ainda mais aprimorado. Isso irá possibilitar uma ampla gama de aplicações e usuários.



# ESPECIFICAÇÕES/REQUISITOS DO SISTEMA - (BAREMA):

__(1) Arquitetura da solução (componentes e mensagens)__  
_Como a arquitetura foi desenvolvida. Quais os componentes e como eles se comunicam. Qual a ordem das mensagens trocadas?_   
A arquitetura desenvolvida consiste em três componentes principais: o client, o broker e o device. Eles interagem da seguinte forma:

   ![Diagrama de Comunicação](./Fluxo%20comunicação.png)

* Client:
    O cliente se comunica com o broker-servidor por meio de requisições HTTP, utilizando as rotas fornecidas pelo servidor para realizar ações como inscrever-se em um tópico, desinscrever-se, solicitar mensagens, ligar sensor etc.  
   O cliente recebe as respostas via request/response HTTP, com o servidor enviando respostas que podem incluir confirmações de sucesso ou falha, mensagens de erro, dados de temperatura, ou qualquer outra informação relevante para a operação solicitada. 

* Broker:
    O servidor é responsável por gerenciar as inscrições em tópicos, rotear mensagens do sensor para os clientes inscritos nos tópicos e lidar com as solicitações dos clientes.
    Ele fornece várias rotas HTTP para que os clientes possam interagir, como inscrever-se em um tópico, desinscrever-se, controlar o sensor, solicitar mensagens etc.
    Além disso, o servidor atua como intermediário entre o sensor e os clientes, recebendo as mensagens do sensor e enviando-as aos clientes inscritos nos tópicos correspondentes.
    O armazenamento de dados mais importante estará no servidor, que o dicionário de tópicos que relaciona os sensores com os clientes, juntamente com suas respectivas mensagens.  
     Quando o cliente manda uma solicitação para controlar o sensor, o broker envia um comando de gerenciamento via TCP para ligar, desligar ou alterar a temperatura do sensor.

*  Sensor:
    O sensor é responsável por coletar dados (temperatura, neste caso) e enviar esses dados para o servidor. 
    Ele se comunica com o servidor por meio de mensagens UDP, enviando dados formatados para o servidor.
    O sensor também possui um socket TCP para aceitar comandos de gerenciamento do servidor, como ligar ou desligar o sensor e alterar dados do sensor.

*   A ordem das mensagens trocadas é a seguinte:

    * O sensor inicia e envia uma mensagem UDP para o servidor informando sobre sua existência e sobre o tópico que ele irá criar para enviar as mensagens.
    * O servidor recebe essa mensagem e cria uma entrada para o tópico correspondente.
    * O cliente se comunica com o servidor por meio de requisições HTTP para se inscrever em um tópico, depois disso ele pode utilizar as demais funcionalidades como controlar o sensor(ligar, desligar, alterar os dados enviados), solicitar mensagens etc.
    * Quando o sensor está ligado, ele envia periodicamente mensagens UDP para o servidor com os dados coletados (temperatura).
    * O servidor recebe essas mensagens e as encaminha para a lista de mensagens pendentes dos clientes inscritos no tópico, cada cliente registrado tem sua própria lista de mensagens pendentes.
    * O cliente pode solicitar mensagens do tópico em que está inscrito, e o servidor responde com as mensagens disponíveis na lista de mensagens pendentes.


  

__(2) Protocolo de comunicação entre dispositivo e Broker - camada de aplicação__  
_Que protocolos de comunicação foram desenvolvidos entre os dispositivos e o broker. Como é a "conversa" entre os dispositivos e o broker?_  
Entre os dispositivos (aplicação) e o broker, foi utilizado o HTTP.  

* Protocolo HTTP (Hypertext Transfer Protocol):  
    O protocolo HTTP é utilizado para que os clientes/aplicação realizem solicitações de inscrição em tópicos, desinscrição de tópicos, controle do dispositivo e obtenção de mensagens do broker.  
    A "conversa" entre os clientes/aplicação e o broker utilizando HTTP ocorre por meio de requisições HTTP, como POST, GET e PUT, enviadas pelos clientes para os endpoints específicos do broker.  
    Por exemplo, um cliente pode enviar uma requisição POST para se inscrever em um tópico, ou uma requisição GET para obter as mensagens de um tópico.
    O broker, por sua vez, processa essas requisições e executa as operações correspondentes, como adicionar ou remover um cliente de um tópico, controlar o dispositivo ou retornar as mensagens pendentes.



__(3) Protocolo de comunicação entre dispositivo e Broker - camada de transporte__  
_Que protocolos de comunicação foram utilizados entre os dispositivos e o broker. TPC e/ou UDP? Em que situações e porque?_  
No sistema proposto, foram desenvolvidos dois protocolos de comunicação distintos entre os dispositivos (sensores) e o broker (servidor):

* __Protocolo de Comunicação UDP entre Dispositivos e Broker:__  
  Este protocolo é utilizado para que os dispositivos (sensores) informem sua existência e enviem dados para o broker (servidor).  
  A conversa entre os dispositivos e o broker ocorre da seguinte maneira:
  
    - O dispositivo inicializa e cria um socket UDP.  
    - Quando ele está executando, o sensor possui um menu para criar um tópico, ligar, desligar e alterar temperatura.  
    - Quando o sensor cria um tópico, é enviada uma mensagem de registro para endereço IP e porta do broker, e o tópico é criado no dicionário de registro que está no broker.  
    - Em seguida, se o dispositivo for ligado, ele envia mensagens UDP formatada em JSON para o broker, com os dados (temperatura), o tópico que vai encaminhar a mensagem, e a ação que ligar.  
    - O servidor recebe essa mensagem e processa as informações, colocando essas mensagens na lista de mensagens pendentes de cada cliente inscrito (se houver) no tópico correspondentes. Essa lista de mensagens pendentes está no dicionário de registro (topic_subscriptions).
    
O envio de dados de sensoriamento, como leituras de temperatura, é uma operação contínua, onde a prioridade é a eficiência e  velocidade de transmissão. Onde, perdas ocasionais de pacotes não são críticas, pois novos dados serão gerados em intervalos regulares. O UDP é adequado para este fim, pois permite o envio rápido e assíncrono de dados, sem a sobrecarga adicional associada ao TCP. 



* __Protocolo de Comunicação TCP entre Dispositivos e Broker para Comandos de Gerenciamento:__
  Este protocolo é utilizado para que o broker (servidor) envie comandos de gerenciamento para os dispositivos (sensores), como ligar/desligar o sensor e alterar dados do sensor.  
 A conversa entre os dispositivos e o broker ocorre da seguinte maneira:

   - O dispositivo cria um socket TCP e fica aguardando conexões.  
   - Quando o broker envia um comando de gerenciamento para um dispositivo específico (mediante a requisição de um cliente), ele estabelece uma conexão TCP com o dispositivo.  
   - O broker envia o comando de gerenciamento (por exemplo, "ligar", "desligar" ou alteração de dados, mas nesse caso o broker só recebe o dado que vai ser alterado, ex: 11 que é referente a temperatura a ser atualizada) para o dispositivo por meio da conexão TCP.  
   - O dispositivo recebe o comando, interpreta e executa a ação correspondente.  
   - Após a execução do comando, o dispositivo fecha a conexão TCP.  
  

A escolha de usar o TCP para os comandos de gerenciamento deve-se ao fato de que essas operações são críticas, exigindo confiabilidade e garantia de entrega.  
Portanto, o uso do TCP é adequado para assegurar a correta execução desses comandos e manter o estado do dispositivo de forma segura.



__(4) Interface da Aplicação (REST)__  
_Quais são os verbos e rotas executados na camada de aplicação?_

Na camada de aplicação, a interface da aplicação utiliza uma arquitetura REST (Representational State Transfer), que utiliza os seguintes verbos HTTP para operações:

POST: Utilizado para criar novos recursos ou enviar dados para um recurso.
GET: Utilizado para recuperar dados de um recurso.
PUT: Utilizado para atualizar um recurso existente com novos dados.
DELETE: Utilizado para excluir um recurso existente.

* Rotas e os verbos HTTP executados na camada de aplicação:
   - /subscribe:
    Verbo: POST
   Descrição: Inscreve um cliente em um tópico específico.
   - /unsubscribe:
    Verbo: POST
   Descrição: Desinscreve um cliente de um tópico específico.
   - /display_topics:
    Verbo: GET
   Descrição: Exibe os tópicos criados.
   - /control_device:
    Verbo: PUT
    Descrição: Controla um dispositivo (ligar, desligar ou alterar temperatura).
   - /get_messages:
    Verbo: GET
   Descrição: Obtém as mensagens de um tópico específico para um cliente.

__(5) Formatação, envio e tratamento de dados__  
_Que tipo de formatação foi usada para transmitir os dados, permitindo que nós diferentes compreendam as mensagens trocadas._

*  Para permitir que nós diferentes compreendam as mensagens trocadas entre os dispositivos e o broker na camada de aplicação, foi utilizada a formatação de dados em JSON (JavaScript Object Notation).

    O JSON é um formato leve e de fácil leitura para intercâmbio de dados entre sistemas. Ele consiste em pares de chave-valor e listas ordenadas de valores. Essa estrutura de dados é facilmente interpretada por várias linguagens de programação, tornando-a ideal para comunicação entre sistemas.

    * Na comunicação HTTP entre o dispositivo cliente e o broker, o formato JSON foi utilizado da seguinte forma:
        data = request.get_json() # captura o payload enviado
        topic = data.get('topic') # extrai o tópico
        action = data.get('action')  # Ação: 'ligar' ou 'desligar'
        ip = data.get('ip')  # Extrai o ip
        port = data.get('port') # Extrai a porta
    
      __A Maioria das rotas possuem essa estrutura__



*   Para a comunicação UDP entre dispositivos (sensores) e broker o padrão da mensagem segue uma estrutura em dicionário. Cada mensagem contém campos específicos que indicam o tipo de ação a ser realizada, o tópico relacionado à mensagem e o conteúdo. Abaixo estão as estruturas das mensagens:

*   Função send_menssage
    ** message ={"action": "ação", "topic": "tópico", "content": "conteúdo"}

    * action: Este campo indica a ação a ser realizada, como "ligar", "desligar".
    * topic: Este campo indica o tópico relacionado à mensagem, que é o nome do sensor
    * content: Este campo contém o conteúdo relevante da mensagem, que pode variar dependendo da ação e do contexto, mas a utilização principal dele nessa função é o envio de dados do sensor para o broker, a outra utilização é só para enviar uma mensagem para atualizar o status do dispositivo depois dele ser desligado pelo broker via tcp.

    Aqui está as aplicações dessa função:
    * Essa chamada de função, send_message(NAME_TOPIC, data, 'Ligar'), tem como objetivo enviar o comando 'Ligar' para atualizar o dicionário no no broker. O conteúdo data enviado junto com o comando será armazenado nas mensagens pendentes de cada cliente por meio do tópico especificado NAME_TOPIC.

    * Essa chamada de função, send_message(NAME_TOPIC, None, 'Desligar'), envia uma mensagem destinada a atualizar o dicionário no broker, indicando que o dispositivo está desligado. Ao enviar None como conteúdo da mensagem foi somente para dizer que não vai existir dados enviados para clientes.

    Outra estrutura utilizada na comunicação UDP, foi a função que cria um tópico para o sensor:
*   Função create_topic
    ** message = {'action': 'subscribe', 'topic': topic, 'ip': TCP_SERVER_IP, 'porta': TCP_SERVER_PORT} # passa a porta para receber comando tcp
    
    Essa função irá mandar a ação de 'subscribe', para se inscrever no tópico,  o tópico específico, e o ip e a porta que irão receber os comandos de gerenciamentos futuros via TCP.


*    Para a comunicação TCP entre dispositivos (sensores) e broker, a estrutura usada foi somente uma string referente aos comandos de gerenciamento. 
    Aplicações: tcp_socket.send('Desligar'.encode()) 
                tcp_socket.send('Ligar'.encode())
                tcp_socket.send(str_change.encode()) # Para enviar nova temperatura para o sensor


  __(6) Tratamento de conexões simultâneas  (threads)__  
_Como threads foram usados para tornar o sistema mais eficiente? Há problemas de concorrência decorrentes do uso de threads? Se sim, como estas
questões foram tratadas?_

As threads foram utilizadas no sistema para lidar com a necessidade de paralelismo entre os códigos. Abaixo está como as threads foram usadas para tornar o sistema mais eficiente:

*  API Flask: threading.Thread(target=start_flask)
    * A API Flask é executada em uma thread separada. Isso permite que o servidor Flask continue a responder às solicitações HTTP dos clientes enquanto o servidor UDP continua a funcionar recebendo e processando mensagens do sensor.
    Como o Flask é um servidor web que lida com solicitações HTTP, é importante executá-lo em uma thread separada para evitar bloqueios no servidor principal(broker).

* Socket TCP do sensor: threading.Thread(target=process_tcp_connection, args=(connection,)).start()
    * O socket TCP usa threads para lidar com as conexões com o broker. Isso permite que o socket se conecte e receba comandos de gerenciamento ao mesmo tempo que o menu está em loop e enviando dados via UDP para o broker.
    
* Buscar mensagens pendentes do cliente: threading.Thread(target=thread_get_messages, args=(stop_event, topics[tupla[1]]))
    * Neste trecho de código, uma nova thread é criada e iniciada para buscar mensagens continuamente do tópico especificado, chamando a rota de receber mensagens dentro de um loop. Isso permite que o cliente receba mensagens sem interromper a execução do restante do programa.
    * O loop principal do programa aguarda até que o usuário pressione Enter, momento em que o evento stop_event é sinalizado para interromper a busca contínua de mensagens.

Não existe problemas de concorrência identificadas.



__(7) Gerenciamento do dispositivo__  
_É possível gerenciar o dispositivo (parar, alterar valores, etc) ? Isso pode ser feito remotamente? E via uma interface do próprio dispositivo?_
    
É possível gerenciar o dispositivo remotamente através da API implementada. O cliente pode fazer requisições para envio de comandos para ligar, desligar e alterar valores do dispositivo via API do broker que irá mandar os comandos de gerenciamento via TCP.

A interface do proprio dispositivo funciona corretamente, ambos podem ligar, desligar e alterar dados de envio do sensor simultaneamente.




__(8) Desempenho (uso de cache no Broker, filas, threads, etc.)__  
_O sistema utiliza algum mecanismos para melhorar o tempo de resposta para a aplicação?_  
    No geral, o uso de threads e a arquitetura assíncrona do servidor UDP e Flask contribuem para um melhor desempenho e tempo de resposta mais rápido para a aplicação. 


__(9) Confiabilidade da solução (tratamento das conexões)__
_Tirando e recolocando o cabo de algum dos nós, o sistema continua funcionando?_  

Ao retirar a rede do broker o sensor continua normalmente, sem aparecer erros, mas o cliente para de funcionar, mas quando a conexão com rede é estabelecida, tudo volta a funcionar normalmente, sem necessidade de executar novamente.

Ao retirar a rede do sensor nenhum erro aparece, ao retomar a conexão tudo os dados não voltam a chegar ao broker, é necessário reiniciar o sensor.

Ao retirar a rede do cliente o erro aparece, mas quando a conexão é estabelecida ele volta a funcionar normalmente, sem necessitar de executar novamente.

O grande pórem é que pode ocorrer de o cliente fazer uma requisição, e se o servidor não estiver em execução, a execução do cliente irá apresentar falhas. 
