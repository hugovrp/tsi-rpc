import os
import sys

# Adiciona o diretório pai ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import config
from tcp_client import rpc_connection
from common.enums import Math_Enum

data_config = config.load_config()

HOST = data_config['ip']
PORT = data_config['port']

def cache_operation(cmd):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return self._process_operation(cmd, *args, use_cache=True, **kwargs)
        return wrapper
    return decorator

class Operations:
    def __init__(self, ip=HOST, port=PORT):
        self.ip = ip
        self.port = port

    def _process_operation(self, cmd, *args, use_cache:bool=False):
        str_args = ' '.join(str(a) for a in args)   
        return rpc_connection(f'{cmd} {str_args}', self.ip, self.port, use_cache=use_cache)
        
    @cache_operation(Math_Enum.SUM.value)
    def sum(self, *args):
        return self._process_operation(Math_Enum.SUM.value, *args)
    
    @cache_operation(Math_Enum.SUB.value)
    def sub(self, *args):
        return self._process_operation(Math_Enum.SUB.value, *args)
    
    @cache_operation(Math_Enum.PROD.value)
    def prod(self, *args):
        return self._process_operation(Math_Enum.PROD.value, *args)

    @cache_operation(Math_Enum.DIV.value)
    def div(self, *args):
        return self._process_operation(Math_Enum.DIV.value, *args)

    @cache_operation(Math_Enum.FAT.value)
    def fat(self, n=None):
        if n is None:
            return 'Erro: É necessário fornecer um número para calcular o fatorial'
        return self._process_operation(Math_Enum.FAT.value, n)
    
    #@cache_operation(Math_Enum.PRIM.value)
    def prim(self, *args):
        return self._process_operation(Math_Enum.PRIM.value, *args, use_cache = False)

    @cache_operation('news')
    def news(self):
        return self._process_operation('news', use_cache=True)
    
            