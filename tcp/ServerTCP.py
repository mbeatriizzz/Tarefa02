import socket
import threading

class Estatisticas:
    def __init__(self):
        self.acertos = {}
        self.erros = {}

    def adicionar_respostas(self, numero_questao, acertos, erros):
        self.acertos[numero_questao] = self.acertos.get(numero_questao, 0) + acertos
        self.erros[numero_questao] = self.erros.get(numero_questao, 0) + erros

    def obter_estatisticas(self):
        return self.acertos, self.erros

def handle_client_connection(client_socket, estatisticas):

    while True:
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            break

        try:
            numero_questao, numero_alternativas, respostas = data.split(';')
            acertos = respostas.count('V')
            erros = respostas.count('F')
            estatisticas.adicionar_respostas(numero_questao, acertos, erros)

            # Envia a resposta 
            resposta = f"{numero_questao};{acertos};{erros}"
            client_socket.send(resposta.encode('utf-8'))
        except:
            client_socket.send("Erro na formatação do questionário".encode('utf-8'))

    client_socket.close()

def main():
    host = 'localhost'
    port = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    estatisticas = Estatisticas()

    print(f"Servidor aguardando conexões em {host}:{port}")

    while True:

        client_socket, addr = server_socket.accept()
        print(f"Conexão estabelecida com {addr[0]}:{addr[1]}")

        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, estatisticas))
        client_thread.start()

if __name__ == '__main__':
    main()
