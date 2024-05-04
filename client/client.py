import requests
import time
import threading

# Configurações
BROKER_URL = 'http://localhost:5000'
CLIENT_PORT = 12340
CLIENT_IP = '127.0.0.1'


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



def exibir_topicos():
    
    try:
        response = requests.get(f'{BROKER_URL}/display_topics')
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
def ligar_sensor(topic):
    response = requests.put(f'{BROKER_URL}/control_device', json={'topic': topic, 'acao': 'ligar'})
    if response.status_code == 200:
        print('Sensor ligado com sucesso via API do broker')
    else:
        print('Erro ao ligar o sensor via API do broker')





# Função para desligar o sensor via API do broker
def desligar_sensor(topic):
    response = requests.put(f'{BROKER_URL}/control_device', json={'topic': topic, 'acao': 'desligar'})
    if response.status_code == 200:
        print('Sensor desligado com sucesso via API do broker')
    else:
        print('Erro ao desligar o sensor via API do broker')




def verificar_inscricao(topic, ip, porta):
    try:
        # Envia a solicitação GET para a rota
        response = requests.get(f'{BROKER_URL}/check_registration', json={'topic': topic, 'ip': ip, 'porta': porta})
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








def get_messages_from_topic(topic, ip, port):

    # Envia a solicitação GET para o servidor
    response = requests.get(f'{BROKER_URL}/get_messages', json={'topic': topic, 'ip': ip, 'port': port})

    # Verifica se a solicitação foi bem-sucedida (código de status HTTP 200)
    if response.status_code == 200:
        # Obtém as mensagens da resposta
        messages = response.json().get('messages', [])
        if messages:
            print(f'Mensagens recebidas do tópico "{topic}":')
            #for message in messages:
            print(messages)
        else:
            print(f'Não há mensagens pendentes no tópico "{topic}" para o cliente {ip}:{port}')
    else:
        print(f'Erro ao obter mensagens do tópico "{topic}": {response.json()['error']}')




def thread_get_messages(event, topic, ip, port):
    while not event.is_set():
        get_messages_from_topic(topic, ip, port)
        time.sleep(4)  # Aguarda 4 segundo antes de buscar mensagens novamente


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




# Menu principal
def main_menu():
    print("=== Menu ===")
    print("1. Inscrever-se em um tópico")
    print("2. Desinscrever-se em um tópico")
    print("3. Ligar sensor")
    print("4. Desligar sensor")
    print('5. Exibir Tópicos')
    print('6. Exibir menssagem')
    print("7. Exibir menssagem continuamente")
    print("8. Sair")

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
                    
        
    elif choice == "3":
        topicos = exibir_topicos()
        print(topicos)
        if topicos == {}:
            print('Não existe tópicos registrados')
        else:
            cod = input("Digite o cod do tópico: ")
            for chave in topicos:
                if cod == chave:
                    # Chama a função para verificar a inscrição do cliente no tópico
                    dic = verificar_inscricao(topicos[cod], CLIENT_IP, CLIENT_PORT)
                    if dic['inscrito']:
                        ligar_sensor(topicos[cod])
                    else:
                        print("Você precisa estar inscrito no tópico para ligar o sensor.")
       

    elif choice == "4":
        topicos = exibir_topicos()
        print(topicos)
        if topicos == {}:
            print('Não existe tópicos registrados')
        else:
            cod = input("Digite o cod do tópico: ")
            for chave in topicos:
                if cod == chave:
                    # Chama a função para verificar a inscrição do cliente no tópico
                    dic = verificar_inscricao(topicos[cod], CLIENT_IP, CLIENT_PORT)
                    if dic['inscrito']:
                        desligar_sensor(topicos[cod])
                    else:
                        print("Você precisa estar inscrito no tópico para desligar o sensor.")

    elif choice == "5":
        print(exibir_topicos())
        

    elif choice == "6":
        topicos = exibir_topicos()
        print(topicos)
        if topicos == {}:
            print('Não existe tópicos registrados')
        else:
            cod = input("Digite o cod do tópico: ")
            for chave in topicos:
                if cod == chave:
                    dic = verificar_inscricao(topicos[cod], CLIENT_IP, CLIENT_PORT)
                    if dic['inscrito']:
                        get_messages_from_topic(topicos[cod], CLIENT_IP, CLIENT_PORT)
                    else:
                        print("Você precisa estar inscrito no tópico para receber mensagens.")

    elif choice == "7":
        topicos = exibir_topicos()
        print(topicos)
        if topicos == {}:
            print('Não existe tópicos registrados')
        else:
            cod = input("Digite o cod do tópico: ")
            for chave in topicos:
                if cod == chave:
                    dic = verificar_inscricao(topicos[cod], CLIENT_IP, CLIENT_PORT)
                    if dic['inscrito']:
                        # Cria um objeto Event
                        stop_event = threading.Event()
                        # Cria e inicia um novo thread para buscar mensagens continuamente
                        thread = threading.Thread(target=thread_get_messages, args=(stop_event, topicos[cod], CLIENT_IP, CLIENT_PORT))
                        thread.start()
                        input("Pressione Enter para parar o sistema de mensagens continuas.")
                        # Sinaliza o evento para parar o loop no thread
                        stop_event.set()
                    else:
                        print("Você precisa estar inscrito no tópico para receber mensagens.")

    elif choice == "8":
        exit()

    else:
        print("Opção inválida.")

# Função para verificar se o servidor está ativo
def servidor():
    try:
        response = requests.get(f'{BROKER_URL}/verificacao')
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'ativo':
                return True
            else:
                print("O servidor não está ativo.")
                return False
        else:
            print("Erro ao verificar o status do servidor:", response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        print("Erro de conexão:", e)
        return False
 

if __name__ == "__main__":    
    # Verifica se o servidor está ativo
    #if servidor():
        # Inicia o cliente apenas se o servidor estiver ativo
        while True:
            main_menu()
   # else:
     #   print("O servidor não está respondendo. Verifique se está ativo e tente novamente.")

