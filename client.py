import requests

# Configurações do servidor
BROKER_URL = 'http://localhost:5000'

# Função para se inscrever em um tópico
def subscribe_to_topic(topic):
    response = requests.post(f'{BROKER_URL}/subscribe', json={'topic': topic})
    if response.status_code == 200:
        print(f'Inscrição no tópico "{topic}" realizada com sucesso')
    else:
        print('Erro ao se inscrever no tópico')

# Função para ligar o sensor via API do broker
def ligar_sensor_via_api():
    response = requests.post(f'{BROKER_URL}/ligar_sensor')
    if response.status_code == 200:
        print('Solicitação para ligar o sensor enviada ao broker')
    else:
        print('Erro ao solicitar ligar o sensor ao broker')


# Menu principal
def main_menu():
    print("=== Menu ===")
    print("1. Inscrever-se em um tópico")
    print("3. Ligar sensor")
    print("4. Desligar sensor")
    print("5. Sair")

    choice = input("Escolha uma opção: ")
    if choice == "1":
        topic = input("Digite o nome do tópico: ")
        subscribe_to_topic(topic)

    elif choice == "5":
        exit()
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    while True:
        main_menu()
