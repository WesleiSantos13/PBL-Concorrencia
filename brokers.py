import socket
import json
from flask import Flask, request, jsonify
import threading

# Configurações do servidor UDP
SERVER_IP = 'localhost'
SERVER_PORT = 8888

# Dicionário para armazenar as inscrições dos clientes em cada tópico
topic_subscriptions = {}

# Armazena as informaçoes dos sensores
endereco_disp = {}

# Criação do socket UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Associa o socket ao endereço e porta do servidor
server_socket.bind((SERVER_IP, SERVER_PORT))

app = Flask(__name__)

# Rota para inscrever-se em um tópico
@app.route('/subscribe', methods=['POST'])
def subscribe_to_topic():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip') 
    port = data.get('port') 
    
    if topic:
        topic_subscriptions[topic]['clients'][(ip, port)] = []
        print(f'Cliente {ip}:{port} se inscreveu no tópico "{topic}"')
        return jsonify({'message': f'Inscrição no tópico "{topic}" realizada com sucesso'})
    else:
        return jsonify({'error': 'Tópico ou porta não fornecidos'}), 400
    

# Rota para desinscrever o cliente do tópico
@app.route('/desinscrever', methods=['POST'])
def desinscrever_topico():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    porta = data.get('porta')
    
    # O cliente está inscrito no tópico e o tópico existe
    if topic in topic_subscriptions and (ip, porta) in topic_subscriptions[topic]['clients']:
        del topic_subscriptions[topic]['clients'][(ip, porta)]
        print(f'Cliente {ip}:{porta} se desinscreveu no tópico "{topic}"')
        return jsonify({'message': f'Cliente desenscrito do tópico "{topic}" realizada com sucesso'}), 200
    else:
        if topic not in topic_subscriptions:
            return jsonify({f'message': 'Tópico não existe'}), 200    
        elif (ip, porta) in topic_subscriptions[topic]:
            return jsonify({f'message': 'O endereço desse cliente não está registrado no tópico'}), 200


@app.route('/exibir_topicos', methods=['GET'])
def exibir_topicos():
    topics = list(topic_subscriptions.keys())
    return jsonify({'topics': topics})


@app.route('/controlar_sensor', methods=['PUT'])
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
@app.route('/verificar_inscricao', methods=['GET'])
def verificar_inscricao():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    porta = data.get('porta')
    
    # O cliente está inscrito no tópico e o tópico existe
    if topic in topic_subscriptions and (ip, porta) in topic_subscriptions[topic]['clients']:
        return jsonify({'inscrito': True}), 200
    else:
        return jsonify({'inscrito': False}), 200
        

# Rota para o cliente solicitar mensagens de um tópico específico
@app.route('/get_messages', methods=['GET'])
def get_messages():
    data = request.get_json()
    topic = data.get('topic')
    ip = data.get('ip')
    porta = data.get('port')
    if topic in topic_subscriptions:
        if topic_subscriptions[topic]['state']== 'Ligado':
            if topic in topic_subscriptions and (ip, porta) in topic_subscriptions[topic]['clients']:
                # Obtém as mensagens pendentes para o cliente no tópico especificado
                messages = topic_subscriptions[topic]['clients'].get((ip, porta), [])
                # Pega a ultima mensagem
                if  messages != []:
                    last_message = messages[-1]
                # Limpa as mensagens pendentes após obter
                topic_subscriptions[topic]['clients'][(ip, porta)] = []
                return jsonify({'messages': last_message})
            else:
                return jsonify({'messages': []})  # Sem mensagens pendentes
        else:
            return jsonify({'error': 'O sensor está desligado'}), 400


# Rota para o cliente saber que o servidor está ativo
@app.route('/verificacao', methods=['GET'])
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
        porta = message.get('porta')

        # Ação de criar um tópico para o sensor
        if topic not in topic_subscriptions and action == 'subscribe':
            topic_subscriptions[topic] = {'clients': {},'state': 'desligado'}
            print(f'O sensor se inscreveu no tópico "{topic}"')
            
            # Salva a porta e o ip para enviar cmd tcp
            endereco_disp[topic]=(ip, porta)
            print(endereco_disp)
            

        elif topic and action == 'Ligar':
            topic_subscriptions[topic]['state'] = 'Ligado'
            # Verifica se o tópico está registrado e se há clientes inscritos
            if topic in topic_subscriptions and topic_subscriptions[topic]:
                # Adiciona a mensagem pendente à lista de mensagens pendentes para todos os clientes inscritos
                for client in topic_subscriptions[topic]['clients']:
                    topic_subscriptions[topic]['clients'][client].append(content)
                print(f'Mensagem adicionada às mensagens pendentes para o tópico "{topic}"')
            else:
                print(f'Nenhum cliente inscrito no tópico "{topic}" para encaminhar a mensagem')
        
        elif topic and action == 'Desligar':
            topic_subscriptions[topic]['state'] = 'Desligado'

        else:
            print(f'Mensagem recebida de {addr}: {content}')
    except json.JSONDecodeError:
        print(f'Mensagem inválida recebida de {addr}: {data.decode()}')


# Função para iniciar o servidor Flask em uma thread separada
def start_flask():
    app.run(debug=True, use_reloader=False)

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
        print(topic_subscriptions)
