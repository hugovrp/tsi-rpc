"""
    Módulo de configuração do sistema RPC.

    Gerencia o carregamento de configurações a partir de arquivo JSON.
"""

import os 
import json 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "configuracoes.txt")

def load_config() :
    """
        Carrega configurações do sistema a partir de arquivo JSON.
        
        Returns:
            dict: Dicionário com as configurações do sistema contendo:
                - ip (str): Endereço IP do servidor
                - port (int): Porta TCP do servidor
                - max_cache_size (int): Tamanho máximo do cache em bytes
                - cache_expiration (int): Tempo de expiração do cache em minutos
        
        Note:
            Arquivo deve estar em formato JSON válido.
            Caminho: config/configuracoes.txt
    """
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)