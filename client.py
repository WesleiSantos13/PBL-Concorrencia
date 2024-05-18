import requests
import time
import threading
import os
import socket

# Configurações
BROKER_URL = "http://"+ os.getenv('IP_SERVER') +":5555" # Para obter o valor da variável de ambiente para o docker
# Caso for executar na máquina, ou seja, sem docker, coloque o ip da máquina no lugar de os.getenv('IP_SERVER').

# Só para registro
CLIENT_PORT = 12340
CLIENT_IP = socket.gethostbyname(socket.gethostname())


# Função para se inscrever em um tópico
def subscribe_to_topic(topic):
    ip = CLIENT_IP
    port = CLIENT_PORT  
    response = requests.post(f'{BROKER_URL}/subscribe', json={'topic': topic, 'port': port, 'ip': ip})
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(response.json()['error'])


# Função para desinscrever do topico
def unsubscribe_to_topic(topic):
    ip = CLIENT_IP
    port = CLIENT_PORT
    response = requests.post(f'{BROKER_URL}/unsubscribe', json={'topic': topic, 'ip': ip, 'port': port})
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(response.json()['error'])  


# Função para exibir os tópicos registrados
def exibir_topicos():
    
    try:
        response = requests.get(f'{BROKER_URL}/display_topics')
        # Verifica se a solicitação foi bem-sucedida
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


# Função para ligar o sensor via API do broker
def on_device(topic):
    ip = CLIENT_IP
    port = CLIENT_PORT
    response = requests.put(f'{BROKER_URL}/control_device', json={'topic': topic, 'action': 'ligar', 'ip': ip, 'port': port})
    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(response.json()['error']) 


# Função para alterar os dados do sensor via API do broker
def change_data(topic, change):
    ip = CLIENT_IP
    port = CLIENT_PORT
    response = requests.put(f'{BROKER_URL}/control_device', json={'topic': topic, 'action': 'alterar', 'ip': ip, 'port': port, 'change': change})
    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print(response.json()['error'])       


# Função para desligar o sensor via API do broker
def off_device(topic):
    ip = CLIENT_IP
    port = CLIENT_PORT
    response = requests.put(f'{BROKER_URL}/control_device', json={'topic': topic, 'action': 'desligar', 'ip': ip, 'port': port})
    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
       # print('Sensor desligado com sucesso via API do broker')
        print(response.json()['message'])
    else:
       # print('Erro ao desligar o sensor via API do broker')
       print(response.json()['error']) 



# Função para receber a ultima menstagem do sensor
def get_messages_from_topic(topic):
    ip = CLIENT_IP
    port = CLIENT_PORT 
    # Envia a solicitação GET para o servidor
    response = requests.get(f'{BROKER_URL}/get_messages', json={'topic': topic, 'ip': ip, 'port': port})

    # Verifica se a solicitação foi bem-sucedida
    if response.status_code == 200:
        # Obtém as mensagens da resposta
        messages = response.json().get('messages', [])
        print(f'Mensagens recebidas do tópico "{topic}":')
        print(messages)
    else:
        print(response.json()['error'])



# Função para chamar a rota de receber mensagens continuamente, até o usuário pressionar ENTER
def thread_get_messages(event, topic):
    while not event.is_set():
        get_messages_from_topic(topic)
        time.sleep(3)  # Aguarda 3 segundos antes de buscar mensagens novamente


# Função para de escolha de topico
def option_topic(topics):
    print(topics)    
    # Se não existir tópicos
    if topics == {}:
        print('Não existe tópicos registrados')
    else:                                                 
        cod = input("Digite o cod do tópico: ")
        for key in topics:
            if cod == key:
                # Se encontrou o codigo digitado como chave do dicionário
                return (True, cod) # Retorna uma tupla com a confirmação e o codigo do topico
    return (False, None)

# Função para impedir que o usuário digite um dado caractere diferente de numéro
def try_change():
    change = ' '
    while type(change) != float:
        try:
            change = float(input('Digite o novo dado '))
        except ValueError:
            print('Digite um número!')
    return change


# Menu principal
def main_menu():
    print("=== Menu ===")
    print("1. Inscrever-se em um tópico")
    print("2. Desinscrever-se de um tópico")
    print("3. Ligar sensor")
    print("4. Alterar dados de um sensor")
    print("5. Desligar sensor")
    print('6. Exibir Tópicos')
    print('7. Exibir mensagem')
    print("8. Exibir mensagem continuamente")
    print("9. Sair")

    # Inscrever em um tópico
    choice = input("Escolha uma opção: ")
    if choice == "1":
        # Resgata o dicionário de tópicos disponiveis
        topics = exibir_topicos()
        # chama a função de opcoes de topicos
        tupla=option_topic(topics)
        # Se a opção for válida
        if tupla[0]:
            subscribe_to_topic(topics[tupla[1]])
        else:
            print('Opção inválida')

    # Desinscrever de um tópico
    elif choice == "2":
        # Resgata o dicionário de tópicos disponiveis
        topics = exibir_topicos()
        # chama a função de opcoes de topicos
        tupla=option_topic(topics)
        # Se a opção for válida
        if tupla[0]:
            unsubscribe_to_topic(topics[tupla[1]])
        else:
            print('Opção inválida')
                    
    # Ligar sensor   
    elif choice == "3":
        # Resgata o dicionário de tópicos disponiveis
        topics = exibir_topicos()
        # chama a função de opcoes de topicos
        tupla=option_topic(topics)
        # Se a opção for válida
        if tupla[0]:
            on_device(topics[tupla[1]])
        else:
            print('Opção inválida')
                    
    # Alterar dados do sensor
    elif choice == "4":
        # Resgata o dicionário de tópicos disponiveis
        topics = exibir_topicos()
        # chama a função de opcoes de topicos
        tupla=option_topic(topics)
        # Se a opção for válida
        if tupla[0]:
            # Novo dado a ser enviado
            change = try_change()
            change_data(topics[tupla[1]], change)
        else:
            print('Opção inválida')

    # Desligar sensor
    elif choice == "5":
        # Resgata o dicionário de tópicos disponiveis
        topics = exibir_topicos()
        # chama a função de opcoes de topicos
        tupla=option_topic(topics)
        # Se a opção for válida
        if tupla[0]:
            off_device(topics[tupla[1]])
        else:
            print('Opção inválida')


    # Exibir tópicos
    elif choice == "6":
        print(exibir_topicos())
        
    # Exibir mensagem
    elif choice == "7":
        # Resgata o dicionário de tópicos disponiveis
        topics = exibir_topicos()
        # chama a função de opcoes de topicos
        tupla=option_topic(topics)
        # Se a opção for válida
        if tupla[0]:
            get_messages_from_topic(topics[tupla[1]])
        else:
            print('Opção inválida')


                        
    # Exibir mensagem continuamente
    elif choice == "8":
        # Resgata o dicionário de tópicos disponiveis
        topics = exibir_topicos()
        # chama a função de opcoes de topicos
        tupla=option_topic(topics)
        # Se a opção for válida
        if tupla[0]:
            # Cria um objeto Event
            stop_event = threading.Event()
            # Cria e inicia um novo thread para buscar mensagens continuamente
            thread = threading.Thread(target=thread_get_messages, args=(stop_event, topics[tupla[1]]))
            thread.start()
            input("Pressione Enter para parar o sistema de mensagens continuas.")
            # Sinaliza o evento para parar o loop no thread
            stop_event.set()     
        else:
            print('Opção inválida')
                    
        

    elif choice == "9":
        exit()

    else:
        print("Opção inválida.")


 
# EXECUÇÃO
if __name__ == "__main__":    
    while True:
        main_menu()

