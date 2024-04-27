import socket
import json
import time
import threading

sensor = {'Nome': 'Sensor de Umidade', 'Estado': 'Desligado', 'Umidade': 30}

# Configurações do servidor UDP
UDP_SERVER_IP = 'localhost'
UDP_SERVER_PORT = 8888

# Configurações do servidor TCP
TCP_SERVER_IP = 'localhost'
TCP_SERVER_PORT = 12343


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
    umidade = sensor['Umidade']
    while sensor['Estado'] == 'Ligado':
        # Formata os dados para envio
        dados = f'Umidade: {umidade}%'
        send_message(sensor['Nome'], dados, 'Ligar')
        umidade += 1
        sensor['Umidade'] = umidade
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
        print("Sensor desligado.")

# Função para alterar a umidade manualmente
def alterar_umidade():
    nova_umidade = float(input("Digite a nova umidade: "))
    sensor['Umidade'] = nova_umidade
    print("Umidade alterada para:", nova_umidade)

# Função para se inscrever no tópico especificado
def subscribe_to_topic(topic):
    message = {'action': 'subscribe', 'topic': topic, 'ip': TCP_SERVER_IP, 'porta': TCP_SERVER_PORT} 
    sensor_socket.sendto(json.dumps(message).encode(), (UDP_SERVER_IP, UDP_SERVER_PORT))

# Inscreve o sensor no tópico inicial
subscribe_to_topic(sensor['Nome'])

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
    print("3. Alterar umidade manualmente")
    print("4. Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")
    if opcao == '1':
        ligar_sensor()
    elif opcao == '2':
        desligar_sensor()
    elif opcao == '3':
        alterar_umidade()
    elif opcao == '4':
        break
    else:
        print("Opção inválida. Tente novamente.")
