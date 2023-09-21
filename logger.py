import datetime
import threading
import queue

log_queue = queue.Queue()
log_lock = threading.Lock()

def log_worker():
    while True:
        log_entry = log_queue.get()
        with log_lock:
            with open("log/server_log.txt", "a") as log_file:
                log_file.write(log_entry)
        log_queue.task_done()

def log_request(client_addr, method, path, response_code,  server, content_type=None, content_length=None):
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        log_entry = "_____________________________________________________________________\n"

        log_entry += f"{timestamp} - {client_addr[0]}:{client_addr[1]} - [{method} {path}] - {response_code}\n"

        log_entry += f"Server: {server}\n"   
        log_entry += f"Content-Type: {content_type}\n" if content_type else ""
        log_entry += f"Content-Length: {content_length}\n" if content_length else "No Content-Length\n"     
        
        print(f"Request: {log_entry}")  
        with log_lock:
            with open("log/server_log.txt", "a") as log_file:
                log_file.write(log_entry)
    except Exception as e:
        print(f"Failed to write to log: {e}")  
