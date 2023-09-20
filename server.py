import socket
import threading
import os
import datetime

# Pasta base dos arquivos a serem servidos
BASE_DIR = "./server"

# Configurações do servidor
HOST = "localhost"
PORT = 8080
MAX_CONNECTIONS = 5
TIMEOUT = 20

# Lock para sincronizar a escrita no arquivo de log
log_lock = threading.Lock()

# Função para gerar o log
def log_request(client_addr, method, path, response_code):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_addr[0]}:{client_addr[1]} - [{method} {path}] - {response_code}\n"
    
    with log_lock:  # Usando lock para tornar a operação thread-safe
        with open("server_log.txt", "a") as log_file:
            log_file.write(log_entry)

# Função para manipular uma única conexão de cliente
def handle_client(client_socket):
    client_addr = client_socket.getpeername()
    request = client_socket.recv(1024).decode()

    # Inicializa variáveis para método e caminho
    method = ""
    path = ""

    # Analisa a requisição
    if request:
        request_lines = request.split("\n")
        first_line = request_lines[0].split()
        method = first_line[0]
        path = first_line[1]

        if method == "GET":
            file_path = os.path.join(BASE_DIR, path[1:])  # Remove a barra inicial

            if os.path.exists(file_path) and os.path.isfile(file_path):
                # Arquivo encontrado, responder com 200 OK
                response_code = "200 OK"
                with open(file_path, "rb") as file:
                    response_data = file.read()
            else:
                # Arquivo não encontrado, responder com 404 Not Found
                response_code = "404 Not Found"
                response_data = b"File not found"
        else:
            # Método não suportado (por exemplo, POST, DELETE), responder com 502 Bad Gateway
            response_code = "502 Bad Gateway"
            response_data = b"Unsupported method"

        # Enviar a resposta ao cliente
        response = f"HTTP/1.1 {response_code}\n\n{response_data.decode()}"
        client_socket.send(response.encode())
        client_socket.close()

        # Registra a requisição no log
        log_request(client_addr, method, path, response_code)
# Função principal do servidor
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