import socket
import json
from flask import Flask, request, jsonify
import threading

# Configurações do servidor UDP
SERVER_IP = 'localhost'
SERVER_PORT = 12345

# Dicionário para armazenar as inscrições dos clientes em cada tópico
topic_subscriptions = {}

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
    addr = request.remote_addr
    if topic:
        if topic not in topic_subscriptions:
            topic_subscriptions[topic] = set()
        topic_subscriptions[topic].add(addr)
        print(f'Cliente {addr} se inscreveu no tópico "{topic}"')
        return jsonify({'message': f'Inscrição no tópico "{topic}" realizada com sucesso'})
    else:
        return jsonify({'error': 'Tópico não fornecido'}), 400

@app.route('/ligar_sensor', methods=['POST'])



# Função para processar as mensagens recebidas e encaminhá-las aos clientes inscritos
def process_message(data, addr):
    try:
        message = json.loads(data.decode())
        topic = message.get('topic')
        content = message.get('content')
        action = message.get('action')
       

        # Ação de escrever o sensor em um topico
        if topic not in topic_subscriptions and action == 'subscribe':
            topic_subscriptions[topic] = set()
            print(f'O sensor se inscreveu no tópico "{topic}"')
       
        # Ação de enviar mensagem do sensor
        elif topic and action == 'LIGAR':
            if topic_subscriptions[topic]:
                subscribers = topic_subscriptions[topic]
                for subscriber in subscribers:
                    server_socket.sendto(json.dumps({'content': content}).encode(), subscriber)
                print(f'Mensagem encaminhada para {len(subscribers)} cliente(s) inscrito(s) no tópico "{topic}"')

                print(f'Mensagem encaminhada para {len(subscribers)} cliente(s) inscrito(s) no tópico "{topic}"')
            else:
                print(f'Nenhum cliente inscrito no tópico "{topic}" para encaminhar a mensagem')

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
