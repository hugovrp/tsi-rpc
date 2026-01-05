import os
import sys
import json
import socket
from config import config
from common.enums import MathEnum, NewsEnum

servers = {
      "server1": {
            "server_ip": "localhost",
            "server_port": "7777",
            "operations": [MathEnum.SUM.value, MathEnum.SUB.value, MathEnum.PROD.value, MathEnum.DIV.value]
      },
      "server2": {
            "server_ip": "localhost",
            "server_port": "7777",
            "operations": [MathEnum.FAT.value, MathEnum.PRIM.value]
      },
      "server3": {
            "server_ip": "localhost",
            "server_port": "7777",
            "operations": [NewsEnum.NEWS.value]
      }
}

def search_operation_server(servers, operation):
    for server_name, server_data in servers.items():    
        if operation in server_data["operations"]:
            return server_data["server_ip"], server_data["server_port"]
    return None

data_config = config.load_config()

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