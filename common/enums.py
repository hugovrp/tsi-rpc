from enum import Enum

class OperationsEnum(Enum):
    """
        Enumeração de comandos disponíveis no sistema RPC.
        
        Attributes:
            SUM (str): Comando de soma ('sum').
            SUB (str): Comando de subtração ('sub').
            PROD (str): Comando de multiplicação ('prod').
            DIV (str): Comando de divisão ('div').
            FAT (str): Comando de fatorial ('fat').
            PRIM (str): Comando de verificação de primos ('prim').
    """
    SUM = 'sum'
    SUB = 'sub'
    PROD = 'prod'
    DIV = 'div'
    FAT = 'fat'
    PRIM = 'prim'
    SOLVER = 'solver'
    NEWS = 'news'