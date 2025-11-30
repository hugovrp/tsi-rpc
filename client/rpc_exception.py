"""
    Módulo de exceções customizadas para RPC.

    Define exceções específicas para tratamento de erros em operações RPC.
"""

class RPCServerNotFound(Exception):
    """
        Exceção lançada quando o servidor RPC não está acessível.
        
        Args:
            host (str): Endereço IP do servidor inacessível.
            port (int): Porta TCP do servidor inacessível.
    """
    def __init__(self, host, port):
        """
            Inicializa a exceção com informações do servidor.
            
            Args:
                host (str): Endereço IP do servidor.
                port (int): Porta TCP do servidor.
        """
        super().__init__(f'Servidor em {host}:{port} está inativo ou recusou a conexão.')