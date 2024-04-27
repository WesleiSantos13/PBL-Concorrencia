import socket

# Configurações do servidor TCP do sensor
SENSOR_TCP_IP = 'localhost'
SENSOR_TCP_PORT = 12349

# Criação do socket TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SENSOR_TCP_IP, SENSOR_TCP_PORT))

while True:
    # Solicita ao usuário que escolha uma ação
    print("Opções:")
    print("1. Ligar sensor")
    print("2. Desligar sensor")
    print("3. Sair")
    opcao = input("Digite o número correspondente à opção desejada: ")

    # Envia o comando correspondente ao sensor
    if opcao == '1':
        client_socket.send('Ligar'.encode())
        print("Comando para ligar o sensor enviado.")
    elif opcao == '2':
        client_socket.send('Desligar'.encode())
        print("Comando para desligar o sensor enviado.")
    elif opcao == '3':
        break
    else:
        print("Opção inválida. Tente novamente.")

# Fecha o socket
client_socket.close()
