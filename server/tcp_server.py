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
    """
        Carrega cache do arquivo JSON no disco.
        
        Args:
            f (str): Caminho do arquivo de cache.
        
        Returns:
            dict: Dicionário com operações cacheadas ou vazio em caso de erro.
    """
    if os.path.exists(f):
        try:
            with open(f, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(f, cache):
    """
        Salva cache no arquivo JSON no disco.
        
        Args:
            f (str): Caminho do arquivo de cache.
            cache (dict): Dicionário com dados a serem salvos.
    """
    with open(f, 'w') as f:
        json.dump(cache, f, indent=4)

def enforce_cache_limit(cache: dict, f: str, max_size: int, new_key: str, new_value):
    """
        Gerencia limite de tamanho do cache usando política FIFO.
        
        Remove entradas antigas se necessário para manter o cache dentro do limite configurado. 
        Valida se nova entrada cabe antes de adicionar.
        
        Args:
            cache (dict): Cache atual em memória.
            f (str): Caminho do arquivo de cache.
            max_size (int): Tamanho máximo do cache em bytes.
            new_key (str): Chave da nova entrada.
            new_value (any): Valor da nova entrada.
        
        Returns:
            bool: True se entrada foi adicionada com sucesso, False caso contrário.
        
        Note:
            - Valida tamanho da nova entrada individualmente
            - Remove entrada mais antiga (FIFO) se necessário
            - Não adiciona se entrada sozinha excede limite
    """

    # Valida tamanho da nova entrada
    temp_single = {new_key: new_value}
    
    temp_file = 'temp_cache_check.json'
    with open(temp_file, 'w') as tf:
        json.dump(temp_single, tf)
    
    new_entry_size = os.path.getsize(temp_file)
    os.remove(temp_file)  
    
    if new_entry_size > max_size:
        print(f'Aviso: A entrada "{new_key}" é muito grande para o cache (tamanho: {new_entry_size} bytes, limite: {max_size} bytes)')
        return False
    
    # Tenta adicionar ao cache existente
    temp_cache = cache.copy()
    temp_cache[new_key] = new_value
    
    save_cache(f, temp_cache)
    new_size = os.path.getsize(f)
    
    if new_size <= max_size:
        cache[new_key] = new_value
        return True
    
    # Remove entrada mais antiga (FIFO)
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
operations_cache = load_cache(CACHE_FILE)
data_config = config.load_config()

HOST = data_config['ip']
PORT = data_config['port']
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