import socket
import json
import time
import threading

sensor = {'Nome': 'Sensor de Temperatura', 'Estado': 'Desligado', 'Temperatura': 24}

# Configurações do servidor UDP
SERVER_IP = 'localhost'
SERVER_PORT = 8888

INITIAL_TOPIC = 'Sensor de Temperatura'

# Criação do socket UDP
sensor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Função para enviar mensagens ao servidor
def send_message(topic, content, action):
    message = {'topic': topic, 'content': content, 'action': action}
    sensor_socket.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))

# Função para simular a leitura de dados do sensor
def ler_dados_sensor():
    temperatura = sensor['Temperatura']
    while sensor['Estado'] == 'Ligado':
        # Formata os dados para envio
        dados = f'Temperatura: {temperatura:.2f}°C'
        send_message(INITIAL_TOPIC, dados, 'Ligar')
        temperatura += 3.1
        temperatura = round(temperatura, 2)
        sensor['Temperatura'] =temperatura
        time.sleep(2)

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

# Função para alterar a temperatura manualmente
def alterar_temperatura():
    nova_temperatura = float(input("Digite a nova temperatura: "))
    sensor['Temperatura'] = nova_temperatura
    print("Temperatura alterada para:", nova_temperatura)

# Função para se inscrever no tópico especificado
def subscribe_to_topic(topic):
    message = {'action': 'subscribe', 'topic': topic}
    sensor_socket.sendto(json.dumps(message).encode(), (SERVER_IP, SERVER_PORT))

# Inscreve o sensor no tópico inicial
subscribe_to_topic(INITIAL_TOPIC)

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
