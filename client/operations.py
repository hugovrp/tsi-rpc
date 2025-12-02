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
    """
        Decorator que habilita cache para operações RPC.
        
        Wraps uma função para automaticamente usar cache ao processar a operação RPC correspondente.
        
        Args:
            cmd (str): Comando da operação (ex: 'sum', 'sub', 'prod').
        
        Returns:
            function: Função decorada com cache habilitado.
    """
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            return self._process_operation(cmd, *args, use_cache=True, **kwargs)
        return wrapper
    return decorator

class Operations:
    """
        Classe principal para executar operações RPC no servidor.
        
        Fornece métodos para realizar operações matemáticas e buscar notícias através de conexão TCP com o servidor remoto.
        
        Attributes:
            ip (str): Endereço IP do servidor.
            port (int): Porta TCP do servidor.
    """

    def __init__(self, ip=HOST, port=PORT):
        """
            Inicializa o cliente de operações RPC.
            
            Args:
                ip (str, optional): Endereço IP do servidor. 
                port (int, optional): Porta TCP do servidor. 
        """
        self.ip = ip
        self.port = port

    def _process_operation(self, cmd, *args, use_cache:bool=False):
        """
            Processa uma operação RPC enviando comando ao servidor.
            
            Método interno que formata o comando com argumentos e envia ao servidor via TCP.
            
            Args:
                cmd (str): Comando da operação (ex: 'sum', 'fat').
                *args: Argumentos variáveis para a operação.
                use_cache (bool, optional): Se deve usar cache. Padrão: False.
            
            Returns:
                any: Resultado retornado pelo servidor.
        """
        str_args = ' '.join(str(a) for a in args)   
        return rpc_connection(f'{cmd} {str_args}', self.ip, self.port, use_cache=use_cache)
        
    @cache_operation(Math_Enum.SUM.value)
    def sum(self, *args):
        """
        Realiza a soma de múltiplos números.
        
        Args:
            *args (float | int): Números a serem somados.
        
        Returns:
            float: Resultado da soma.
            str: Mensagem de erro se nenhum argumento fornecido.
        
        Raises:
            RPCServerNotFound: Se o servidor estiver offline e sem cache.
        """
        return self._process_operation(Math_Enum.SUM.value, *args)
    
    @cache_operation(Math_Enum.SUB.value)
    def sub(self, *args):
        """
            Realiza a subtração sequencial de múltiplos números.
            
            Subtrai o segundo número do primeiro, depois o terceiro do resultado, e assim por diante.
            
            Args:
                *args (float | int): Números a serem subtraídos sequencialmente.
            
            Returns:
                float: Resultado da subtração.
                str: Mensagem de erro se nenhum argumento fornecido.
            
            Raises:
                RPCServerNotFound: Se o servidor estiver offline e sem cache.
        """
        return self._process_operation(Math_Enum.SUB.value, *args)
    
    @cache_operation(Math_Enum.PROD.value)
    def prod(self, *args):
        """
            Realiza a multiplicação de múltiplos números.
            
            Args:
                *args (float | int): Números a serem multiplicados.
            
            Returns:
                float: Resultado da multiplicação.
                str: Mensagem de erro se nenhum argumento fornecido.
            
            Raises:
                RPCServerNotFound: Se o servidor estiver offline e sem cache.
        """
        return self._process_operation(Math_Enum.PROD.value, *args)

    @cache_operation(Math_Enum.DIV.value)
    def div(self, *args):
        """
        Realiza a divisão sequencial de múltiplos números.
        
        Divide o primeiro número pelo segundo, depois o resultado pelo terceiro, e assim por diante.
        
        Args:
            *args (float | int): Números para divisão sequencial.
        
        Returns:
            float: Resultado da divisão.
            str: Mensagem de erro se divisão por zero ou sem argumentos.
        
        Raises:
            RPCServerNotFound: Se o servidor estiver offline e sem cache.
        """
        return self._process_operation(Math_Enum.DIV.value, *args)

    @cache_operation(Math_Enum.FAT.value)
    def fat(self, n=None):
        """
            Calcula o fatorial de um número.
            
            Args:
                n (int, optional): Número inteiro não-negativo.
            
            Returns:
                int: Fatorial de n (n!).
                str: Mensagem de erro se n for None, negativo ou inválido.
            
            Raises:
                RPCServerNotFound: Se o servidor estiver offline e sem cache.
        """
        if n is None:
            return 'Erro: É necessário fornecer um número para calcular o fatorial'
        return self._process_operation(Math_Enum.FAT.value, n)
    
    #@cache_operation(Math_Enum.PRIM.value)
    def prim(self, *args):
        """
            Verifica se números são primos usando processamento paralelo.
            
            Args:
                *args (int): Números inteiros a serem verificados.
            
            Returns:
                list[bool]: Lista de booleanos indicando se cada número é primo.
            
            Raises:
                RPCServerNotFound: Se o servidor estiver offline.
        """
        return self._process_operation(Math_Enum.PRIM.value, *args, use_cache = False)

    @cache_operation('news')
    def news(self):
        """
            Obtém as principais manchetes de notícias do UOL.
            
            Faz web scraping do site UOL e retorna as 5 principais manchetes.
            O resultado é cacheado para evitar requisições excessivas.
            
            Returns:
                list[str]: Lista com até 5 manchetes de notícias.
                list[str]: Lista com mensagem de erro em caso de falha.
            
            Raises:
                RPCServerNotFound: Se o servidor estiver offline e sem cache.
            
            Note:
                Esta operação depende da conectividade do servidor com a internet.
        """
        return self._process_operation('news', use_cache=True)
    
            