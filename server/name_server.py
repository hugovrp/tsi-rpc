import os
import sys
import json
import socket
from config import config
from common.enums import OperationsEnum

data_config = config.load_config()

# Mapeamento de servidores e suas operações suportadas
servers = {
      "server1": {
            "server_ip": data_config['ip_server1'],
            "server_port": data_config['port_server1'],
            "operations": [OperationsEnum.SUM.value, OperationsEnum.SUB.value, OperationsEnum.PROD.value, OperationsEnum.DIV.value]
      },
      "server2": {
            "server_ip": data_config['ip_server2'],
            "server_port": data_config['port_server2'],
            "operations": [OperationsEnum.FAT.value, OperationsEnum.PRIM.value]
      },
      "server3": {
            "server_ip": data_config['ip_server3'],
            "server_port": data_config['port_server3'],
            "operations": [OperationsEnum.SOLVER.value, OperationsEnum.NEWS.value]
      }
}

def search_operation_server(servers, operation):
    """
        Busca o servidor responsável por processar uma operação específica.
        
        Itera sobre o dicionário de servidores registrados e retorna as informações de conexão do primeiro servidor 
        que suporta a operação solicitada.
        
        Args:
            servers (dict): Dicionário com configuração dos servidores.
                Formato: {
                    "server_name": {
                        "server_ip": str,
                        "server_port": int,
                        "operations": list[str]
                    }
                }
            operation (str): Nome da operação a ser buscada.
                               
        Returns:
            tuple[str, int] | None: Tupla (ip, porta) do servidor responsável.
                                    Retorna None se a operação não for encontrada em nenhum servidor registrado.
        
        Note:
            Retorna o PRIMEIRO servidor encontrado que suporta a operação.
            Se múltiplos servidores suportarem a mesma operação, apenas o primeiro será retornado (comportamento de busca linear).
    """
    for server_name, server_data in servers.items():    
        if operation in server_data['operations']:
            return server_data['server_ip'], server_data['server_port']
    return None

HOST = data_config['ip_name_server']
PORT = data_config['port_name_server']

# Loop principal do servidor
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ns_socket:
    ns_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    ns_socket.bind((HOST, PORT))
    print(f"Servidor UDP escutando em {HOST}:{PORT}")

    while True:
        data, addr = ns_socket.recvfrom(1024 * 1024)

        operation = data.decode().strip()
        result = search_operation_server(servers, operation)

        if result:
            server_ip, server_port = result
            response = {
                "server_ip": server_ip,
                "server_port": server_port
            }
        else:
            response = {
                "error": "Operação não suportada"
            }
          
        ns_socket.sendto(json.dumps(response).encode(), addr)