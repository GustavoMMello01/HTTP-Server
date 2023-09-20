from handlers import handle_client
import socket
import threading

# Configurações do servidor
HOST = "localhost"
PORT = 8080
MAX_CONNECTIONS = 5
TIMEOUT = 20

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(MAX_CONNECTIONS)

    print(f"Servidor HTTP rodando em http://{HOST}:{PORT}")

    while True:
        client_socket, client_addr = server_socket.accept()
        client_socket.settimeout(TIMEOUT)
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    main()
