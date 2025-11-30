class RPCServerNotFound(Exception):
    def __init__(self, host, port):
        super().__init__(f'Servidor em {host}:{port} está inativo ou recusou a conexão.')