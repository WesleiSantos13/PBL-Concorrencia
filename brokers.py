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
    addr = request.remote_addr  # Obtém o endereço IP do cliente
    port = data.get('port')  # Obtém a porta do cliente do corpo da solicitação JSON
    print(port)
    if topic and port:
        if topic not in topic_subscriptions:
            topic_subscriptions[topic] = set()
        # Armazena uma tupla contendo o endereço IP e a porta do cliente
        topic_subscriptions[topic].add((addr, port))
        print(f'Cliente {addr}:{port} se inscreveu no tópico "{topic}"')
        return jsonify({'message': f'Inscrição no tópico "{topic}" realizada com sucesso'})
    else:
        return jsonify({'error': 'Tópico ou porta não fornecidos'}), 400

@app.route('/exibir_topicos', methods=['GET'])
def exibir_topicos():
    topics = list(topic_subscriptions.keys())
    return jsonify({'topics': topics})


# Rota para ligar o sensor via TCP
@app.route('/ligar_sensor', methods=['POST'])
def ligar_sensor():
    data = request.get_json()
    topic = data.get('topic')
    SENSOR_TCP_IP = endereco_disp[topic][0]
    SENSOR_TCP_PORT = endereco_disp[topic][1]

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SENSOR_TCP_IP, SENSOR_TCP_PORT))
        client_socket.send('Ligar'.encode())
        client_socket.close()
        return jsonify({'message': 'Comando para ligar o sensor enviado via TCP'})
    except Exception as e:
        return jsonify({'error': f'Erro ao ligar o sensor via TCP: {str(e)}'}), 500

# Rota para desligar o sensor via TCP
@app.route('/desligar_sensor', methods=['POST'])
def desligar_sensor():
    SENSOR_TCP_IP = 'localhost'
    SENSOR_TCP_PORT = 12349
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SENSOR_TCP_IP, SENSOR_TCP_PORT))
        client_socket.send('Desligar'.encode())
        client_socket.close()
        return jsonify({'message': 'Comando para desligar o sensor enviado via TCP'})
    except Exception as e:
        return jsonify({'error': f'Erro ao desligar o sensor via TCP: {str(e)}'}), 500
        


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
            topic_subscriptions[topic] = set()
            print(f'O sensor se inscreveu no tópico "{topic}"')
            # Salva a porta e o ip para enviar cmd tcp
            endereco_disp[topic]=(ip, porta)
            print(endereco_disp)
            

        # Ação de enviar mensagem do sensor
        elif topic and action == 'Ligar':
            print(topic_subscriptions)
            if topic not in topic_subscriptions:
                topic_subscriptions[topic] = set()
            elif topic in topic_subscriptions and topic_subscriptions[topic] != set():  
                subscribers = topic_subscriptions[topic]
                for subscriber in subscribers:
                    server_socket.sendto(json.dumps({'content': content}).encode(), subscriber)

                print(f'Mensagem encaminhada para {len(subscribers)} cliente(s) inscrito(s) no tópico "{topic}"')
            else:
                print(f'Nenhum cliente inscrito no tópico "{topic}" para encaminhar a mensagem')
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
