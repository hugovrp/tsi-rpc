import os
import sys
import json
import socket
from datetime import datetime, timedelta

# Adiciona o diretório pai ao sys.path para enxergar a pasta 'config'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config
import rpc_exception

CACHE_FILE = 'cache_operations.json'

operations_cache = {}
data_config = config.load_config()
CACHE_EXPIRATION_MINUTES = data_config.get('cache_expiration', 10)

def load_disk_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def rpc_connection(command:str, host, port, use_cache:bool = True):
    if use_cache and command in operations_cache:
        cache_entry = operations_cache[command]
        timestamp = datetime.fromisoformat(cache_entry['timestamp'])
        if datetime.now() - timestamp < timedelta(minutes=CACHE_EXPIRATION_MINUTES):
            print('Retornando do cache em memória (cliente).')
            return cache_entry['response']
    
    disk_cache = load_disk_cache()
    try:
        check_status_server(host, port)
    except rpc_exception.RPCServerNotFound:
        if use_cache and command in disk_cache:
            cache_entry = disk_cache[command]
            print('Servidor offline, usando cache de disco (servidor).')
            return cache_entry
        raise
        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        client_socket.sendall((command).encode())

        raw_response = client_socket.recv(1024 * 1024).decode().strip()

        try:
            response = json.loads(raw_response)
        except json.JSONDecodeError:
            response = raw_response

        if use_cache:
            cache_data = {
                'response': response,
                'timestamp': datetime.now().isoformat()
            }
            operations_cache[command] = cache_data

        return response

def check_status_server(host, port, timeout=2):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        raise rpc_exception.RPCServerNotFound(host, port) from None
