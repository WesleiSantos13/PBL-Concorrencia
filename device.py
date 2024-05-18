import socket
import json
import time
import threading
import os


# Configurações iniciais do sensor
device = {'Nome': ' ', 'Estado': 'Desligado', 'Temperatura': 24, 'Registrado': False}
                                                                                        # 'Registrado' serve para saber se o sensor criou 
                                                            #                                 um tópico
# O nome será definido depois de obter a porta tcp de conexão


# Configurações do servidor UDP para enviar a temperatura  
UDP_SERVER_IP = os.getenv('IP_SERVER') # Para obter o valor da variável de ambiente para o docker
# Caso for executar na máquina, ou seja, sem docker, coloque o ip da máquina no lugar de os.getenv('IP_SERVER').
UDP_SERVER_PORT = 8888

# Configurações do servidor TCP para receber comandos de gerenciamento
TCP_SERVER_IP = socket.gethostbyname(socket.gethostname())

# Criação do socket UDP
device_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Criação do socket TCP
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server_socket.bind((TCP_SERVER_IP, 0))
tcp_server_socket.listen(1)  # Escuta apenas uma conexão por vez

# Obtém a porta à qual o socket foi vinculado
TCP_SERVER_PORT = tcp_server_socket.getsockname()[1]

# Altera o nome do sensor, para garantir que não tenham sensores com o mesmo nome
device['Nome']= 'Sensor-Temp-'+str(TCP_SERVER_PORT) #adiciona a porta no nome para diferenciar dos outros dispositivos

# O nome do tópico que o sensor vai criar possui o mesmo nome do sensor
NAME_TOPIC = device['Nome']

# Função para enviar mensagens ao servidor (UDP)
def send_message(topic, content, action):
    message = {'topic': topic, 'content': content, 'action': action}
    device_socket.sendto(json.dumps(message).encode(), (UDP_SERVER_IP, UDP_SERVER_PORT))

# Função para simular a leitura de dados do sensor
def reading_device():
    while device['Estado'] == 'Ligado':
        temperatura = device['Temperatura']
        # Formata os dados para envio
        data = f'Temperatura: {temperatura:.2f}°C'
        # Envia a mensagem para o servidor
        send_message(NAME_TOPIC, data, 'Ligar')
        temperatura += 3.1
        temperatura = round(temperatura, 2)
        # Atualiza a temperatura no dicionário
        device['Temperatura'] = temperatura
        time.sleep(2)

# Função para lidar com conexões TCP
def process_tcp_connection(connection):
    while True:
        data = connection.recv(1024).decode()
        print(data)
        if not data:
            break
        print("Mensagem recebida do servidor:", data)
        if data == 'Ligar':
            on_device()
        elif data == 'Desligar':
            off_device()
        else:
            device['Temperatura'] = float(data)
            print('Temperatura atualizada')
    connection.close()

# Função para ligar o sensor
def on_device():
    if device['Estado'] == 'Desligado':
        device['Estado'] = 'Ligado'
        threading.Thread(target=reading_device).start()
        print("Sensor ligado.")

# Função para desligar o sensor
def off_device():
    if device['Estado'] == 'Ligado':
        device['Estado'] = 'Desligado'
        # Manda uma mensagem apenas para atualizar o dicionário que está no servidor, para informar que o dispositivo está desligado
        send_message(NAME_TOPIC, None, 'Desligar')
        print("Sensor desligado.")

# Função para alterar a temperatura manualmente
def change_temperature():
    new_temperature = float(input("Digite a nova temperatura: "))
    device['Temperatura'] = new_temperature
    print("Temperatura alterada para:", new_temperature)

# Função para criar um tópico para envio de temperatura
def create_topic(topic):
    message = {'action': 'subscribe', 'topic': topic, 'ip': TCP_SERVER_IP, 'porta': TCP_SERVER_PORT} # passa a porta e o ip para receber comando tcp
    device_socket.sendto(json.dumps(message).encode(), (UDP_SERVER_IP, UDP_SERVER_PORT))



# Thread para lidar com conexões TCP
def tcp_server_thread():
    while True:
        connection, address = tcp_server_socket.accept()
        print("Conexão TCP estabelecida com:", address)
        threading.Thread(target=process_tcp_connection, args=(connection,)).start()

# Inicia a thread do servidor TCP, para que o sensor receba mensagens em outra thread
threading.Thread(target=tcp_server_thread).start()

# Loop principal
while True:
    print("Opções:")
    print("0. Criar um tópico para enviar mensagem")
    print("1. Ligar sensor")
    print("2. Desligar sensor")
    print("3. Alterar temperatura manualmente")
    print("4. Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")
   
   # Criar tópico 
    if opcao == '0':   
        create_topic(NAME_TOPIC)
        device['Registrado'] = True

        print(f"Tópico {NAME_TOPIC} criado com sucesso")

    elif opcao == '1' and device['Registrado']:
        on_device()
    
    elif opcao == '2' and device['Registrado']:
        off_device()
    
    elif opcao == '3':
        change_temperature()
    
    elif opcao == '4':
        break
    
    elif opcao not in ('0','1','2','3','4'):
        print("Opção inválida. Tente novamente.")
        
    else:
        print('O sensor não está registrado em um tópico')
