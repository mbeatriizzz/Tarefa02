import threading
import socket

def main():
    endereco_servidor = 'localhost'
    porta_servidor = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        client.connect((endereco_servidor, porta_servidor))
    except:
        return print('\nNão foi possível se conectar ao servidor!\n')

    username = input('Usuário> ')  
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=(client,))
    thread2 = threading.Thread(target=sendMessages, args=(client, username))

    thread1.start()
    thread2.start()

def receiveMessages(client):  
    while True:
        try:
            msg, _ = client.recvfrom(2048)
            msg = msg.decode('utf-8')
            print(msg + '\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('\nPressione <Enter> para continuar...')
            client.close()
            break

def sendMessages(client, username):
    while True:
        try:
            numero_questao = input('Número da questão: ')
            numero_alternativas = input('Número de alternativas: ')
            respostas = input('Respostas: ')

            mensagem = f"{numero_questao};{numero_alternativas};{respostas}"
            client.sendto(mensagem.encode('utf-8'), ('localhost', 12345))
        except:
            return

main()
