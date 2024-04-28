import threading
import requests
import socket
import json
from queue import Queue

# Configurações
BROKER_URL = 'http://localhost:5000'
CLIENT_PORT = 12340
CLIENT_IP = '127.0.0.1'

# Criando socket UDP para receber mensagens
receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receive_socket.bind((CLIENT_IP, CLIENT_PORT))

# Criando uma fila para passar as mensagens do thread de recebimento para o thread principal
message_queue = Queue()

# Função para se inscrever em um tópico
def subscribe_to_topic(topic):
    ip = CLIENT_IP
    port = CLIENT_PORT  
    response = requests.post(f'{BROKER_URL}/subscribe', json={'topic': topic, 'port': port, 'ip': ip})
    if response.status_code == 200:
        print(f'Inscrito no tópico "{topic}" com sucesso')
    else:
        print('Erro ao se inscrever no tópico')


def verificar_inscricao(topic, ip, porta):
    try:
        # Envia a solicitação GET para a rota
        response = requests.get(f'{BROKER_URL}/verificar_inscricao', json={'topic': topic, 'ip': ip, 'porta': porta})
        if response.status_code == 200:
            return response.json()
        else:
            # Se a resposta não for bem-sucedida, imprime o código de status e retorna False
            print(f"Erro: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        # Em caso de erro de conexão, imprime o erro e retorna False
        print(f"Erro de conexão: {e}")
        return False




# Função para desinscrever do topico
def desinscrever_topic(topic, ip, porta):
    response = requests.post(f'{BROKER_URL}/desinscrever', json={'topic': topic, 'ip': ip, 'porta': porta})
    message = response.json()['message']
    print(message)


# Função para ligar o sensor via API do broker
def ligar_sensor(topic):
    response = requests.post(f'{BROKER_URL}/ligar_sensor', json={'topic': topic})
    if response.status_code == 200:
        print('Sensor ligado com sucesso via API do broker')
    else:
        print('Erro ao ligar o sensor via API do broker')

# Função para desligar o sensor via API do broker
def desligar_sensor(topic):
    response = requests.post(f'{BROKER_URL}/desligar_sensor', json={'topic': topic})
    if response.status_code == 200:
        print('Sensor desligado com sucesso via API do broker')
    else:
        print('Erro ao desligar o sensor via API do broker')


def exibir_topicos():
    
    try:
        response = requests.get(f'{BROKER_URL}/exibir_topicos')
        if response.status_code == 200:  # Verifica se a solicitação foi bem-sucedida
            dic={}
            data = response.json()  # Converte a resposta para JSON
            topics = data.get('topics', [])  # Obtém a lista de tópicos
            for c in range(0, len(topics)):
                chave = c+1
                dic[str(chave)]=topics[c]
            
            return dic
        else:
            print(f"Erro ao obter tópicos: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")




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
    print("2. Desinscrever-se em um tópico")
    print("3. Ligar sensor")
    print("4. Desligar sensor")
    print('5. Exibir Tópicos')
    print("6. Sair")

    choice = input("Escolha uma opção: ")
    if choice == "1":
        topicos = exibir_topicos()
        print(topicos)
        if topicos == {}:
            print('Não existe tópicos registrados')
        else:
            cod = input("Digite o cod do tópico: ")
            for chave in topicos:
                if cod ==chave:
                    subscribe_to_topic(topicos[cod])
    
    elif choice == "2":
        topic = input("Digite o nome do tópico que deseja desinscrever: ")
        desinscrever_topic(topic, CLIENT_IP, CLIENT_PORT)
        
    elif choice == "3":
        topic = input("Digite o nome do tópico para ligar o sensor: ")
        # Chama a função para verificar a inscrição do cliente no tópico
        dic = verificar_inscricao(topic, CLIENT_IP, CLIENT_PORT)
        if dic['inscrito']:
            ligar_sensor(topic)
        else:
            print("Você precisa estar inscrito no tópico para ligar o sensor.")
       

    elif choice == "4":
        topic = input("Digite o nome do tópico para desligar o sensor: ")
        # Chama a função para verificar a inscrição do cliente no tópico
        dic = verificar_inscricao(topic, CLIENT_IP, CLIENT_PORT)
        if dic['inscrito']:
            desligar_sensor(topic)
        else:
            print("Você precisa estar inscrito no tópico para desligar o sensor.")

    elif choice == "5":
        print(exibir_topicos())

    elif choice == "6":
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
