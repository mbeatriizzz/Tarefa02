import threading
import socket
from multiprocessing import Manager

def main():
    endereco_servidor = 'localhost'
    porta_servidor = 12345

    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind((endereco_servidor, porta_servidor))

    print(f"Servidor UDP iniciado em {endereco_servidor}:{porta_servidor}")

    estatisticas = Manager().dict()

    thread1 = threading.Thread(target=receiveResponses, args=(server, estatisticas))
    thread2 = threading.Thread(target=sendStatistics, args=(estatisticas,))

    thread1.start()
    thread2.start()

def receiveResponses(server, estatisticas):
    while True:
        dados, endereco_cliente = server.recvfrom(2048)
        mensagem = dados.decode('utf-8')
        numero_questao, _, respostas = mensagem.split(';')
        acertos = respostas.count('V')
        erros = respostas.count('F')
        resposta = f"{numero_questao};{acertos};{erros}".encode('utf-8')

        estatisticas[numero_questao] = (acertos, erros)

        server.sendto(resposta, endereco_cliente)

def sendStatistics(estatisticas):
    while True:
        input("\nPressione Enter para exibir as estatísticas:")
        print("Estatísticas:")
        for numero_questao, (acertos, erros) in estatisticas.items():
            print(f"Questão {numero_questao}: acertos={acertos} erros={erros}")

if __name__ == "__main__":
    main()
