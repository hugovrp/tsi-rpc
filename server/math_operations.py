"""
    Módulo de operações matemáticas para o servidor RPC.

    Implementa a lógica de negócio para todas as operações matemáticas suportadas pelo sistema, incluindo processamento paralelo para
    verificação de números primos.
"""

import os
import sys
import math
import multiprocessing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.enums import Math_Enum

sys.set_int_max_str_digits(1000000)

def _is_prime(n):
    """
        Verifica se um número é primo (função auxiliar interna).
        
        Utilizada internamente pelo pool de multiprocessing.
        
        Args:
            n (int): Número a ser verificado.
        
        Returns:
            bool: True se o número é primo, False caso contrário.
        
        Note:
            Números menores que 2 não são considerados primos.
            Usa algoritmo de tentativa de divisão até raiz quadrada.
    """
    if n < 2:
        return False
    
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def check_primes(number):
    """
        Wrapper público para verificação de número primo.
        
        Args:
            number (int): Número a ser verificado.
        
        Returns:
            bool: True se o número é primo, False caso contrário.
    """
    return _is_prime(number)

def math_operations(data):
    """
        Processa comando matemático e retorna resultado.
        
        Parser principal que recebe string de comando, identifica a operação e executa o cálculo correspondente.
        
        Args:
            data (str): String com comando e argumentos separados por espaço.
                        Formato: "comando arg1 arg2 arg3 ..."
                        Comandos válidos: sum, sub, prod, div, fat, prim
        
        Returns:
            float: Resultado para operações aritméticas (sum, sub, prod, div).
            int: Resultado para fatorial (fat).
            list[bool]: Lista de booleanos para verificação de primos (prim).
            str: Mensagem de erro em caso de falha.
        
        Raises:
            Não lança exceções diretamente, retorna strings de erro.
        
        Note:
            - Operação 'prim' usa multiprocessing com pool de 4 processos
            - Suporta números muito grandes (até 1.000.000 dígitos)
            - Divisão por zero retorna mensagem de erro
            - Fatorial de números negativos retorna erro
    """
    try:
        parts = data.strip().split()
        
        cmd = parts[0]
        args = parts[1:]  

        if cmd == Math_Enum.SUM.value:
            if not args:
                return 'Erro: A operação requer pelo menos um número'
            
            nums = [float(a) for a in args]
            return sum(nums)
    
        elif cmd == Math_Enum.SUB.value:
            if not args:
                return 'Erro: A operação requer pelo menos um número'
            
            nums = [float(a) for a in args]
            total = nums[0]
            for i in nums[1:]:
                total -= i
            return total

        elif cmd == Math_Enum.PROD.value:
            if not args:
                return 'Erro: A operação requer pelo menos um número'

            nums = [float(a) for a in args]
            total = nums[0]
            for i in nums[1:]:
                total *= i
            return total
        elif cmd == Math_Enum.DIV.value:
            if not args:
                return 'Erro: A operação requer pelo menos um número'

            nums = [float(a) for a in args]
            total = nums[0]
            for i in nums[1:]:
                try:
                    total /= i
                except ZeroDivisionError:
                    return "Erro: Divisão por zero não é permitida."
            return total
        elif cmd == Math_Enum.FAT.value:
            num = int(args[0])
            if num < 0:
                return "Erro: fatorial não é definido para números negativos"
            return math.factorial(num)
        elif cmd == Math_Enum.PRIM.value:
            numbers_list = [int(i) for i in args]

            with multiprocessing.Pool(processes=4) as pool:
                result = pool.map(check_primes, numbers_list)

            return result
        else:
            return '\nErro: Comando desconhecido!\n'
    except:
        return 'Erro'

