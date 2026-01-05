import os
import json
import socket
import requests
from bs4 import BeautifulSoup
from config import config, cache_config

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SERVER_DIR, 'cache_operations.json')

def get_news():
    """
        Obtém manchetes de notícias do site UOL via web scraping.
        
        Faz requisição HTTP ao UOL, parseia HTML e extrai as principais manchetes das tags <h3>.
        
        Returns:
            list[str]: Lista com até 5 manchetes de notícias.
                       Retorna mensagem de erro em caso de falha.
        
        Note:
            Requer conexão com a internet.
            Retorna lista vazia com mensagem se nenhuma notícia encontrada.
    """
    try:
        response = requests.get('https://www.uol.com.br')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        headlines = [a.get_text(strip=True) for a in soup.find_all('h3') if a.get_text(strip=True)]
        
        return headlines[:5] or ['Nenhuma notícia encontrada!']
    except Exception as e:
        return [f'Erro ao obter as notícias: {e}'] 

# Inicialização do servidor
operations_cache = cache_config.load_cache(CACHE_FILE)
data_config = config.load_config()

HOST = data_config['ip_server3']
PORT = data_config['port_server3']
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

            if data.strip() == 'news':
                if 'news' in operations_cache:
                    response = operations_cache['news']
                else:
                    response = get_news()
                    cache_config.enforce_cache_limit(operations_cache, CACHE_FILE, MAX_CACHE_SIZE, 'news', response)

                conn.send(json.dumps(response).encode())
                continue