import os
import sys
import json

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