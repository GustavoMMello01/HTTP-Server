import datetime
import threading

# Lock para sincronizar a escrita no arquivo de log
log_lock = threading.Lock()

def log_request(client_addr, method, path, response_code):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} - {client_addr[0]}:{client_addr[1]} - [{method} {path}] - {response_code}\n"
    
    with log_lock:
        with open("log/server_log.txt", "a") as log_file:
            log_file.write(log_entry)
