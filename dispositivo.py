import socket
import json
import time
import threading

# Configurações do servidor UDP
SERVER_IP = 'localhost'
SERVER_PORT = 12345
BROKER_IP = 'localhost'
BROKER_PORT = 12346
SENSOR_COMMAND_PORT = 12347
INITIAL_TOPIC = 'Sensor de Temperatura'

# Criação do socket UDP
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Variáveis para armazenar os valores de temperatura e umidade
temperatura = 25.5
umidade = 60.0

# Variável para controlar se o sensor está ligado ou desligado
sensor_ligado = False

# Função para enviar mensagens ao servidor
def send_message(topic, content, action):
    #client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = {'topic': topic, 'content': content, 'action': action}
    sensor_socket.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))

# Função para se conectar ao broker e aguardar comandos de ligar e desligar o sensor
def conectar_e_aguardar_comandos():
    global sensor_ligado
    sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sensor_socket.bind((SERVER_IP, SENSOR_COMMAND_PORT))
    print("Aguardando comandos do broker...")
    while True:
        data, addr = sensor_socket.recvfrom(1024)
        message = json.loads(data.decode())
        action = message.get('action')
        if action == 'ligar':
            ligar_sensor()
        elif action == 'desligar':
            desligar_sensor()

# Função para simular a leitura de dados do sensor
def ler_dados_sensor():
    global temperatura
    while sensor_ligado:
        # Formata os dados para envio
        dados = f'Temperatura: {temperatura:.2f}°C'
        send_message(INITIAL_TOPIC, dados, 'LIGAR')
        temperatura += 3.1
        temperatura = round(temperatura, 2)
        time.sleep(2)

# Função para ligar o sensor
def ligar_sensor():
    global sensor_ligado
    if not sensor_ligado:
        sensor_ligado = True
        threading.Thread(target=ler_dados_sensor).start()
        print("Sensor ligado.")

# Função para desligar o sensor
def desligar_sensor():
    global sensor_ligado
    if sensor_ligado:
        sensor_ligado = False
        print("Sensor desligado.")

# Função para se inscrever no tópico especificado
def subscribe_to_topic(topic):
    message = {'action': 'subscribe', 'topic': topic}
    sensor_socket.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))


# Thread para se conectar ao broker e aguardar comandos
thread_conectar_broker = threading.Thread(target=conectar_e_aguardar_comandos)
thread_conectar_broker.start()

# Inscreve o sensor no tópico inicial
subscribe_to_topic(INITIAL_TOPIC)

# Loop principal
while True:
    print("Opções:")
    print("1. Ligar sensor")
    print("2. Desligar sensor")
    print("3. Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")
    if opcao == '1':
        ligar_sensor()
    elif opcao == '2':
        desligar_sensor()
    elif opcao == '3':
        break
    else:
        print("Opção inválida. Tente novamente.")
