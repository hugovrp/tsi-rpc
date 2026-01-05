import os
import sys
import json
import socket
from datetime import datetime, timedelta
from config import config
from client.rpc_exception import RPCServerNotFound

CACHE_FILE = 'cache_operations.json'

operations_cache = {}
data_config = config.load_config()
CACHE_EXPIRATION_MINUTES = data_config.get('cache_expiration', 10)

def load_disk_cache():
    """
        Carrega o cache persistente do disco.
        
        Tenta ler o arquivo de cache JSON do servidor. Se houver erro ou arquivo não existir, retorna dicionário vazio.
        
        Returns:
            dict: Dicionário com operações cacheadas ou vazio.
    """
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def dns_connection(operation:str, host, port, use_cache:bool = True):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

        parts = operation.strip().split()
        cmd = parts[0]

        client_socket.sendto((cmd).encode(), (host, port))

        data, addr = client_socket.recvfrom(1024 * 1024)

        response = json.loads(data.decode())

        server_ip = response["server_ip"]
        server_port = int(response["server_port"])

        return rpc_connection(operation, server_ip, server_port, use_cache)

def rpc_connection(command:str, host, port, use_cache:bool = True):
    """
        Estabelece conexão RPC com o servidor via TCP.
        
        Implementa sistema de cache em memória com expiração por tempo.
        Em caso de servidor offline, tenta usar cache em disco do servidor.
        
        Args:
            command (str): Comando a ser executado (ex: "sum 5 2").
            host (str): Endereço IP do servidor.
            port (int): Porta TCP do servidor.
            use_cache (bool, optional): Se deve usar cache. Padrão: True.
        
        Returns:
            any: Resposta do servidor (pode ser string, número, lista, etc).
                 Respostas JSON são automaticamente deserializadas.
        
        Raises:
            RPCServerNotFound: Se servidor offline e sem cache disponível.
        
        Note:
            Cache em memória expira após tempo configurado (padrão: 1 minuto).
            Cache em disco é usado como fallback se servidor offline.
    """

    # Verifica cache em memória
    if use_cache and command in operations_cache:
        cache_entry = operations_cache[command]
        timestamp = datetime.fromisoformat(cache_entry['timestamp'])
        if datetime.now() - timestamp < timedelta(minutes=CACHE_EXPIRATION_MINUTES):
            print('Retornando do cache em memória (cliente).')
            return cache_entry['response']
    
    # Tenta acessar cache em disco se servidor offline
    disk_cache = load_disk_cache()
    try:
        check_status_server(host, port)
    except RPCServerNotFound:
        if use_cache and command in disk_cache:
            cache_entry = disk_cache[command]
            print('Servidor offline, usando cache de disco (servidor).')
            return cache_entry
        raise

    # Conecta ao servidor  
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
    """
        Verifica se o servidor RPC está online e acessível.
        
        Tenta estabelecer conexão TCP com timeout configurável.
        
        Args:
            host (str): Endereço IP do servidor.
            port (int): Porta TCP do servidor.
            timeout (int, optional): Timeout em segundos. Padrão: 2.
        
        Returns:
            bool: True se servidor está acessível.
        
        Raises:
            RPCServerNotFound: Se não conseguir conectar ao servidor.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        raise RPCServerNotFound(host, port) from None
