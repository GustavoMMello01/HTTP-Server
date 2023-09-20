from logger import log_request
import os

BASE_DIR = "./server"

# Manipula conexão de cliente
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
                response_code = "200 OK"
                with open(file_path, "rb") as file:
                    response_data = file.read()
            else:
                response_code = "404 Not Found"
                response_data = b"File not found"
                
        elif method == "PUT": #curl -X PUT -d @put_index.html http://localhost:8080/index.html
            file_path = os.path.join(BASE_DIR, path[1:])
            try:
                with open(file_path, "wb") as file:
                    file.write(b"Resource updated via PUT")
                response_code = "204 No Content"
                response_data = b""
            except FileNotFoundError:
                        response_code = "404 Not Found"
                        response_data = b"File not found"
            except Exception as e:
                response_code = "500 Internal Server Error"
                response_data = b"An error occurred while processing the PUT request"
        
        elif method == "POST":
            file_path = os.path.join(BASE_DIR, path[1:])
            try: 
                with open(file_path, "wb") as file:
                    file.write(b"Resource created via POST")
                response_code = "201 Created"
                response_data = b""
            except Exception as e:
                response_code = "500 Internal Server Error"
                response_data = b"An error occurred while processing the POST request"

        else:
            response_code = "502 Bad Gateway" # metodo nao suportado
            response_data = b"Unsupported method"

        # Enviar a resposta ao cliente
        response = f"HTTP/1.1 {response_code}\n\n{response_data.decode()}"
        client_socket.send(response.encode())
        client_socket.close()

        log_request(client_addr, method, path, response_code)
