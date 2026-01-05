import os
import json
import socket
from config import config, cache_config
from server.math_operations import number_theory

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SERVER_DIR, 'cache_operations.json')

# Inicialização do servidor
operations_cache = cache_config.load_cache(CACHE_FILE)
data_config = config.load_config()

HOST = data_config['ip_server2']
PORT = data_config['port_server2']
MAX_CACHE_SIZE = data_config['max_cache_size']

# Loop principal do servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()
        with conn:
            data = conn.recv(1024 * 1024).decode().strip()

            if not data:
                continue

            if data in operations_cache:
                print('Pegando valor do cache (servidor JSON).')
                response = operations_cache[data]
            else:
                response = number_theory(data)

                cache_config.enforce_cache_limit(operations_cache, CACHE_FILE, MAX_CACHE_SIZE, data, response)
                
            conn.send(str(response).encode())