import threading
import requests
import socket
import json
from queue import Queue

# Configurações
BROKER_URL = 'http://localhost:5000'
CLIENT_PORT = 12340

# Criando socket UDP para receber mensagens
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.bind(('localhost', CLIENT_PORT))

# Criando uma fila para passar as mensagens do thread de recebimento para o thread principal
message_queue = Queue()

# Função para se inscrever em um tópico
def subscribe_to_topic(topic):
    addr = socket.gethostbyname(socket.gethostname())  # Obtém o endereço IP do cliente
    port = CLIENT_PORT  # Obtém a porta do cliente
    response = requests.post(f'{BROKER_URL}/subscribe', json={'topic': topic, 'port': port})
    if response.status_code == 200:
        print(f'Inscrito no tópico "{topic}" com sucesso')
    else:
        print('Erro ao se inscrever no tópico')



# Função para ligar o sensor via API do broker
def turn_on_sensor_via_api():
    response = requests.post(f'{BROKER_URL}/turn_on_sensor')
    if response.status_code == 200:
        print('Solicitação para ligar o sensor enviada ao broker')
    else:
        print('Erro ao solicitar ligar o sensor ao broker')

# Função para receber mensagens do servidor
def receive_messages():
    while True:
        data, addr = receive_socket.recvfrom(1024)
        message = json.loads(data.decode())
        message_queue.put(message["content"])  # Adicionando a mensagem à fila

# Função para exibir mensagens recebidas
def display_messages():
    while True:
        message = message_queue.get()  # Obter mensagem da fila
        print(f'Mensagem recebida do servidor: {message}')

# Menu principal
def main_menu():
    print("=== Menu ===")
    print("1. Inscrever-se em um tópico")
    print("2. Ligar sensor")
    print("3. Desligar sensor")
    print("4. Sair")

    choice = input("Escolha uma opção: ")
    if choice == "1":
        topic = input("Digite o nome do tópico: ")
        subscribe_to_topic(topic)
    elif choice == "2":
        turn_on_sensor_via_api()
    elif choice == "4":
        exit()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    # Iniciando threads para receber mensagens e exibir mensagens
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.daemon = True
    receive_thread.start()

    display_thread = threading.Thread(target=display_messages)
    display_thread.daemon = True
    display_thread.start()

    # Loop do menu principal
    while True:
        main_menu()
