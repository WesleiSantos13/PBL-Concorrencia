import socket
import json
from flask import Flask, request, jsonify
import threading

# Configurações do servidor UDP para receber mensagem
SERVER_IP = 'localhost'
SERVER_PORT = 8888

# Dicionário para armazenar as os topicos pelos quais os sensores irão mandar as mensagens e as inscrições dos clientes em cada tópico
topic_subscriptions = {}

# Armazena as informaçoes dos sensores (nome, endereço e porta)
endereco_disp = {}

# Criação do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço e porta do servidor
server_socket.bind((SERVER_IP, SERVER_PORT))

app = Flask(__name__)






# Rota para inscrever o cliente em um tópico
@app.route('/subscribe', methods=['POST'])
def subscribe_to_topic():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip') 
    port = data.get('port') 
    # Se o cliente já estiver inscrito no tópico
    if (ip,port) in topic_subscriptions[topic]['clients']:
        return jsonify({'error': f'Você já está inscrito no tópico "{topic}" '}), 400
   
    # Se o cliente não estiver inscrito no tópico
    elif (ip,port) not in topic_subscriptions[topic]['clients']:
        topic_subscriptions[topic]['clients'][(ip, port)] = []
        print(f'Cliente ({ip}, {port}) se inscreveu no tópico "{topic}"')
        return jsonify({'message': f'Inscrição no tópico "{topic}" realizada com sucesso'}), 200
    

    



# Rota para desinscrever o cliente do tópico
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe_to_topic():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    port = data.get('port')
    
    # O cliente está inscrito 
    if (ip, port) in topic_subscriptions[topic]['clients']:
        del topic_subscriptions[topic]['clients'][(ip, port)]
        print(f'Cliente ({ip}, {port}) se desinscreveu no tópico "{topic}"')
        return jsonify({'message': f'Cliente desenscrito do tópico "{topic}" '}), 200
    else: 
        return jsonify({f'error': 'O endereço desse cliente não está registrado no tópico'}), 400






# Rota para exibir os tópicos/sensores registrados
@app.route('/display_topics', methods=['GET'])
def exibir_topicos():
    topics = list(topic_subscriptions.keys())
    return jsonify({'topics': topics})




# Rota para ligar ou desligar o dispositivo/sensor
@app.route('/control_device', methods=['PUT'])
def controlar_sensor():
    data = request.get_json()
    topic = data.get('topic')
    action = data.get('action')  # Ação: 'ligar' ou 'desligar'
    ip = data.get('ip')
    port = data.get('port')
    
    # Pega o a porta e o ip do socket tcp para enviar o comando de ligar ou desligar
    SENSOR_TCP_IP = endereco_disp[topic][0]
    SENSOR_TCP_PORT = endereco_disp[topic][1]
    
    # Se o cliente estiver inscrito no tópico, ele pode pedir ao servidor para ligar ou desligar o sensor
    if (ip, port) in topic_subscriptions[topic]['clients']:
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((SENSOR_TCP_IP, SENSOR_TCP_PORT))
            
            # Só ligar se não estiver ligado
            if action == 'ligar' and topic_subscriptions[topic]['state'] != 'Ligado':
                tcp_socket.send('Ligar'.encode())
                tcp_socket.close()
                return jsonify({'message': f'Comando para {action} o sensor enviado via TCP', 'status': topic_subscriptions[topic]['state']})
            # Só desligar se não estiver desligado
            elif action == 'desligar' and topic_subscriptions[topic]['state'] != 'Desligado':
                tcp_socket.send('Desligar'.encode())
                tcp_socket.close()
                return jsonify({'message': f'Comando para {action} o sensor enviado via TCP', 'status': topic_subscriptions[topic]['state']})
            
            else:
                return jsonify({'error': f'o sensor já está sobre o comando {action}'}), 400
            
        except Exception as e:
            return jsonify({'error': f'Erro ao {action} o sensor via TCP: {str(e)}'}), 500
    else:
       return jsonify({'error':f"Você precisa estar inscrito para usar o comando {action}."}), 400





# Rota para o cliente solicitar mensagens de um tópico específico
@app.route('/get_messages', methods=['GET'])
def get_messages():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    port = data.get('port')

    # Se o cliente estiver inscrito no tópico
    if (ip, port) in topic_subscriptions[topic]['clients']:
        # Se o dispositivo estiver ligado
        if topic_subscriptions[topic]['state']== 'Ligado':
            # Obtém as mensagens pendentes para o cliente no tópico especificado
            messages = topic_subscriptions[topic]['clients'].get((ip, port), [])
            if  messages != []:
                # Pega a ultima mensagem
                last_message = messages[-1]
            # Limpa as mensagens pendentes após obter
            topic_subscriptions[topic]['clients'][(ip, port)] = []
            # Envia a mensagem atual
            return jsonify({'messages': last_message}), 200
        else:
            return jsonify({'error': 'O sensor está desligado'}), 400
    else:
       return jsonify({'error':f"Você precisa estar inscrito para solicitar mensagens."}), 400




# Função para processar as mensagens recebidas e encaminhá-las aos clientes inscritos
def process_message(data, addr):
    try:
        message = json.loads(data.decode())
        topic = message.get('topic')
        content = message.get('content')
        action = message.get('action')
        ip = message.get('ip')
        port = message.get('porta')

        # Ação de criar um tópico para o sensor
        if topic not in topic_subscriptions and action == 'subscribe':
            topic_subscriptions[topic] = {'clients': {},'state': 'desligado'}
            print(f'O sensor se inscreveu no tópico "{topic}"')
            
            # Salva a porta e o ip para enviar comandos de gerenciamento via TCP
            endereco_disp[topic]=(ip, port)
            
            
        # Se o sensor estiver ligado mandando mensagem
        elif topic and action == 'Ligar':
            # Se o tópico não estiver criado, o servidor cria, isso foi feito para caso o servidor reinicie e sensor permaneça ligado
            if topic not in topic_subscriptions:
                topic_subscriptions[topic] = {'clients': {},'state': 'desligado'}
           
            # Atualiza o estado do sensor no dicionário de tópicos    
            topic_subscriptions[topic]['state'] = 'Ligado'

            # Verifica se existem clientes registrados para adicionar mensagens
            if topic_subscriptions[topic]['clients'] != {}:
                # Adiciona a mensagem pendente à lista de mensagens pendentes para todos os clientes inscritos
                for client in topic_subscriptions[topic]['clients']:
                    topic_subscriptions[topic]['clients'][client].append(content)
                print(f'Mensagem adicionada às mensagens pendentes para o tópico "{topic}"')
            # Caso não existam clientes registrados
            else:
                print(f'Nenhum cliente inscrito no tópico "{topic}" para encaminhar a mensagem')
        
        # Se o dispositivo estiver desligado
        elif topic and action == 'Desligar':
            # Atualiza o estado do dispositivo no dicionário de topicos dos dispositivos
            topic_subscriptions[topic]['state'] = 'Desligado'

        else:
            print('O Sensor já está inscrito no tópico')
    except json.JSONDecodeError:
        print(f'Mensagem inválida recebida de {addr}: {data.decode()}')


# Função para iniciar o servidor Flask em uma thread separada
def start_flask():
    app.run(debug=True, use_reloader=False)



# Execução
if __name__ == '__main__':
    # Inicia o servidor Flask em uma thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()

    # Loop para receber os dados continuamente
    while True:
        # Recebe os dados do cliente
        data, addr = server_socket.recvfrom(1024)
    
        # Processa os dados recebidos
        process_message(data, addr)
        
        # Exibe o dicionário de topicos
        print(topic_subscriptions)
