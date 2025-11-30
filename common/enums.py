"""
    Módulo de enumerações compartilhadas.

    Define constantes para comandos matemáticos usados em todo o sistema.
"""

from enum import Enum

class Math_Enum(Enum):
    """
        Enumeração de comandos matemáticos disponíveis no sistema RPC.
        
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