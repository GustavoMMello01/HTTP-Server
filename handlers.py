from logger import log_request
import os

BASE_DIR = "./server"

# Manipula conexão de cliente
def handle_client(client_socket):
    server = "server/1.0"
    content_type = ""
    response_length = 0

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
            file_path = os.path.join(BASE_DIR, path[1:])

            if os.path.exists(file_path) and os.path.isfile(file_path):
                response_code = "200 OK"
                with open(file_path, "rb") as file:
                    response_data = file.read()
                
                if file_path.endswith(".html"): #verifica se o arquivo é um html
                    content_type = "text/html"
                elif file_path.endswith(".jpg"): #verifica se o arquivo é uma imagem
                    content_type = "image/jpeg"
                elif file_path.endswith(".mp4"): #verifica se o arquivo é um video
                    content_type = "video/mp4"
                elif file_path.endswith(".mp3"): #verifica se o arquivo é um audio
                    content_type = "audio/mp3"
                
                content_length = len(response_data) # armazena o tamanho do arquivo
            else: #caso o arquivo não exista
                response_code = "404 Not Found" 
                response_data = b"File not found"
                
        elif method == "PUT": #curl -X PUT -d @put_index.html http://localhost:8080/index.html
            file_path = os.path.join(BASE_DIR, path[1:])
            try:
                with open(file_path, "wb") as file: #abre o arquivo para escrita
                    file.write(b"Resource updated via PUT")
                response_code = "204 No Content"
                response_data = b""
            except FileNotFoundError: #caso o arquivo não exista
                        response_code = "404 Not Found"
                        response_data = b"File not found"
            except Exception as e: #caso ocorra algum erro
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
        
        elif method == "DELETE":
            file_path = os.path.join(BASE_DIR, path[1:])
            response_code = "501 Not Implemented"  # Apenas um exemplo de HTTP Response
            response_data = b"DELETE method is not implemented"
        
        elif method == "HEAD":
            file_path = os.path.join(BASE_DIR, path[1:])

            if os.path.exists(file_path) and os.path.isfile(file_path):
                response_code = "200 OK"
                response_data = b""  # O método HEAD não retorna o corpo da resposta, apenas cabeçalhos
                
                if file_path.endswith(".html"):
                    content_type = "text/html"
                elif file_path.endswith(".jpg"):
                    content_type = "image/jpeg"
                elif file_path.endswith(".mp4"):
                    content_type = "video/mp4"
                elif file_path.endswith(".mp3"):
                    content_type = "audio/mp3"
                
                content_length = 0
            else:
                response_code = "404 Not Found"
                response_data = b"File not found"

        else:
            response_code = "502 Bad Gateway" # metodo nao suportado
            response_data = b"Unsupported method"


        # Enviar a resposta ao cliente
        response = f"HTTP/1.1 {response_code}\n\n{response_data.decode()}"
        client_socket.send(response.encode())
        client_socket.close()

        log_request(client_addr, method, path, response_code, server, content_type, content_length)
