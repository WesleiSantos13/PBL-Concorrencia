import socket
import json
import time
import threading

sensor = {'Nome': 'Sensor de Temperatura', 'Estado': 'Desligado', 'Temperatura': 24}

# Configurações do servidor UDP
UDP_SERVER_IP = 'localhost'
UDP_SERVER_PORT = 8888

# Configurações do servidor TCP
TCP_SERVER_IP = 'localhost'
TCP_SERVER_PORT = 12349

INITIAL_TOPIC = sensor['Nome']

# Criação do socket UDP
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Criação do socket TCP
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((TCP_SERVER_IP, TCP_SERVER_PORT))
tcp_server_socket.listen(1)  # Escuta apenas uma conexão por vez

# Função para enviar mensagens ao servidor
def send_message(topic, content, action):
    message = {'topic': topic, 'content': content, 'action': action}
    sensor_socket.sendto(json.dumps(message).encode(), (UDP_SERVER_IP, UDP_SERVER_PORT))

# Função para simular a leitura de dados do sensor
def ler_dados_sensor():
    temperatura = sensor['Temperatura']
    while sensor['Estado'] == 'Ligado':
        # Formata os dados para envio
        dados = f'Temperatura: {temperatura:.2f}°C'
        send_message(INITIAL_TOPIC, dados, 'Ligar')
        temperatura += 3.1
        temperatura = round(temperatura, 2)
        sensor['Temperatura'] = temperatura
        time.sleep(2)

# Função para lidar com conexões TCP
def handle_tcp_connection(connection):
    while True:
        data = connection.recv(1024).decode()
        print(data)
        if not data:
            break
        print("Mensagem recebida do broker:", data)
        if data == 'Ligar':
            ligar_sensor()
        elif data == 'Desligar':
            desligar_sensor()
    connection.close()

# Função para ligar o sensor
def ligar_sensor():
    if sensor['Estado'] == 'Desligado':
        sensor['Estado'] = 'Ligado'
        threading.Thread(target=ler_dados_sensor).start()
        print("Sensor ligado.")

# Função para desligar o sensor
def desligar_sensor():
    if sensor['Estado'] == 'Ligado':
        sensor['Estado'] = 'Desligado'
        send_message(INITIAL_TOPIC, None, 'Desligar')
        print("Sensor desligado.")

# Função para alterar a temperatura manualmente
def alterar_temperatura():
    nova_temperatura = float(input("Digite a nova temperatura: "))
    sensor['Temperatura'] = nova_temperatura
    print("Temperatura alterada para:", nova_temperatura)

# Função para se inscrever no tópico especificado
def subscribe_to_topic(topic):
    message = {'action': 'subscribe', 'topic': topic, 'ip': TCP_SERVER_IP, 'porta': TCP_SERVER_PORT} # passa a porta para receber comando tcp
    sensor_socket.sendto(json.dumps(message).encode(), (UDP_SERVER_IP, UDP_SERVER_PORT))

# Inscreve o sensor no tópico inicial
subscribe_to_topic(INITIAL_TOPIC)

# Thread para lidar com conexões TCP
def tcp_server_thread():
    while True:
        connection, address = tcp_server_socket.accept()
        print("Conexão TCP estabelecida com:", address)
        threading.Thread(target=handle_tcp_connection, args=(connection,)).start()

# Inicia a thread do servidor TCP
threading.Thread(target=tcp_server_thread).start()

# Loop principal
while True:
    print("Opções:")
    print("1. Ligar sensor")
    print("2. Desligar sensor")
    print("3. Alterar temperatura manualmente")
    print("4. Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")
    if opcao == '1':
        ligar_sensor()
    elif opcao == '2':
        desligar_sensor()
    elif opcao == '3':
        alterar_temperatura()
    elif opcao == '4':
        break
    else:
        print("Opção inválida. Tente novamente.")
