import socket

def main():
    host = 'localhost'
    port = 5000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))

        with open('respostas.txt', 'r') as file:
            for line in file:
                data = line.strip().encode('utf-8')
                client_socket.send(data)

                response = client_socket.recv(1024).decode('utf-8')
                print(f"Resposta do servidor: {response}")

    except Exception as e:
        print(f"Ocorreu um erro: {str(e)}")

    finally:
        client_socket.close()

if __name__ == '__main__':
    main()
