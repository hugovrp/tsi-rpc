import os
import sys
import json
import socket
import requests
from bs4 import BeautifulSoup

# Adiciona o diretório pai ao sys.path para enxergar a pasta 'config'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config 
from math_operations import math_operations

CACHE_FILE = 'cache_operations.json'

def load_cache(f):
    if os.path.exists(f):
        try:
            with open(f, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(f, cache):
    with open(f, 'w') as f:
        json.dump(cache, f, indent=4)

def enforce_cache_limit(cache: dict, f: str, max_size: int, new_key: str, new_value):
    temp_single = {new_key: new_value}
    
    temp_file = 'temp_cache_check.json'
    with open(temp_file, 'w') as tf:
        json.dump(temp_single, tf)
    
    new_entry_size = os.path.getsize(temp_file)
    os.remove(temp_file)  
    
    if new_entry_size > max_size:
        print(f'Aviso: A entrada "{new_key}" é muito grande para o cache (tamanho: {new_entry_size} bytes, limite: {max_size} bytes)')
        return False
    
    temp_cache = cache.copy()
    temp_cache[new_key] = new_value
    
    save_cache(f, temp_cache)
    new_size = os.path.getsize(f)
    
    if new_size <= max_size:
        cache[new_key] = new_value
        return True
    
    if cache:  
        oldest_key = next(iter(cache))
        temp_cache_reduced = cache.copy()
        temp_cache_reduced.pop(oldest_key)
        temp_cache_reduced[new_key] = new_value
        
        save_cache(f, temp_cache_reduced)
        reduced_size = os.path.getsize(f)
        
        if reduced_size <= max_size:
            cache.clear()
            cache.update(temp_cache_reduced)
            print(f'Removida entrada antiga "{oldest_key}" para adicionar "{new_key}"')
            return True
    
    save_cache(f, cache)
    print(f'Aviso: Não há espaço suficiente para adicionar "{new_key}" ao cache')
    return False

def get_news():
    try:
        response = requests.get('https://www.uol.com.br')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        headlines = [a.get_text(strip=True) for a in soup.find_all('h3') if a.get_text(strip=True)]
        
        return headlines[:5] or ['Nenhuma notícia encontrada!']
    except Exception as e:
        return [f'Erro ao obter as notícias: {e}'] 

operations_cache = load_cache(CACHE_FILE)
data_config = config.load_config()

HOST = data_config['ip']
PORT = data_config['port']
MAX_CACHE_SIZE = data_config['max_cache_size']

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
                    enforce_cache_limit(operations_cache, CACHE_FILE, MAX_CACHE_SIZE, 'news', response)

                conn.send(json.dumps(response).encode())
                continue

            if data in operations_cache:
                print('Pegando valor do cache (servidor JSON).')
                response = operations_cache[data]
            else :
                response = math_operations(data)

                if not data.startswith('prim'):
                    enforce_cache_limit(operations_cache, CACHE_FILE, MAX_CACHE_SIZE, data, response)
                
            conn.send(str(response).encode())