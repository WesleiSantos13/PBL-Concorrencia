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
    
    if (ip,port) in topic_subscriptions[topic]['clients']:
        return jsonify({'message': f'Você já está inscrito no tópico "{topic}" '})
       
    elif (ip,port) not in topic_subscriptions[topic]['clients']:
        topic_subscriptions[topic]['clients'][(ip, port)] = []
        print(f'Cliente ({ip},{port}) se inscreveu no tópico "{topic}"')
        return jsonify({'message': f'Inscrição no tópico "{topic}" realizada com sucesso'})
    
    else:
        return jsonify({'error': 'Erro ao se inscrever no tópico'}), 400
    



# Rota para desinscrever o cliente do tópico
@app.route('/unsubscribe', methods=['POST'])
def unsubscribe_to_topic():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    port = data.get('port')
    
    # O cliente está inscrito no tópico e o tópico existe
    if topic and ip and port in topic_subscriptions and (ip, port) in topic_subscriptions[topic]['clients']:
        del topic_subscriptions[topic]['clients'][(ip, port)]
        print(f'Cliente {ip}:{port} se desinscreveu no tópico "{topic}"')
        return jsonify({'message': f'Cliente desenscrito do tópico "{topic}" realizada com sucesso'}), 200
    else:
        if topic not in topic_subscriptions:
            return jsonify({f'message': 'Tópico não existe'}), 200    
        elif (ip, port) in topic_subscriptions[topic]:
            return jsonify({f'message': 'O endereço desse cliente não está registrado no tópico'}), 200






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
    acao = data.get('acao')  # Ação: 'ligar' ou 'desligar'
    SENSOR_TCP_IP = endereco_disp[topic][0]
    SENSOR_TCP_PORT = endereco_disp[topic][1]
    
    if topic in topic_subscriptions:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SENSOR_TCP_IP, SENSOR_TCP_PORT))
            
            if acao == 'ligar' and topic_subscriptions[topic]['state'] != 'Ligado':
                client_socket.send('Ligar'.encode())
                #message = 'Sensor ligado'
            elif acao == 'desligar' and topic_subscriptions[topic]['state'] != 'Desligado':
                client_socket.send('Desligar'.encode())
               # message = 'Sensor desligado'
            else:
                return jsonify({'error': 'Ação inválida'}), 400
            
            client_socket.close()
            return jsonify({'message': f'Comando para {acao} o sensor enviado via TCP', 'status': topic_subscriptions[topic]['state']})
        except Exception as e:
            return jsonify({'error': f'Erro ao {acao} o sensor via TCP: {str(e)}'}), 500
    else:
        return jsonify({'message': 'O sensor não existe'})




# Rota para verificar se o cliente está registrado no tópico
@app.route('/check_registration', methods=['GET'])
def verificar_inscricao():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    port = data.get('porta')
    
    # O cliente está inscrito no tópico e o tópico existe
    if topic in topic_subscriptions and (ip, port) in topic_subscriptions[topic]['clients']:
        return jsonify({'inscrito': True}), 200
    else:
        return jsonify({'inscrito': False}), 200
        




# Rota para o cliente solicitar mensagens de um tópico específico
@app.route('/get_messages', methods=['GET'])
def get_messages():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    port = data.get('port')

    if topic in topic_subscriptions:
        if topic_subscriptions[topic]['state']== 'Ligado':
            if topic in topic_subscriptions and (ip, port) in topic_subscriptions[topic]['clients']:
                # Obtém as mensagens pendentes para o cliente no tópico especificado
                messages = topic_subscriptions[topic]['clients'].get((ip, port), [])
                # Pega a ultima mensagem
                if  messages != []:
                    last_message = messages[-1]
                # Limpa as mensagens pendentes após obter
                topic_subscriptions[topic]['clients'][(ip, port)] = []
                return jsonify({'messages': last_message})
            else:
                return jsonify({'messages': []})  # Sem mensagens pendentes
        else:
            return jsonify({'error': 'O sensor está desligado'}), 400







# Rota para o cliente saber que o servidor está ativo
@app.route('/check_server', methods=['GET'])
def verificacao():
    return jsonify({'status': 'ativo'})




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
