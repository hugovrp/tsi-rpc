import os
import sys
import math
import multiprocessing
from common.enums import OperationsEnum

sys.set_int_max_str_digits(1000000)

def _is_prime(n):
    """
        Verifica se um número é primo (função auxiliar interna).
        
        Utilizada internamente pelo pool de multiprocessing na função number_theory() para verificação paralela de múltiplos números.
        
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

def basic_operations(data):
    """
        Executa operações aritméticas básicas a partir de comandos textuais.
        
        Parser que identifica o comando e executa a operação correspondente:
        - sum: soma todos os argumentos
        - sub: subtração sequencial (a - b - c - ...)
        - prod: multiplicação de todos os argumentos
        - div: divisão sequencial (a / b / c / ...)
        
        Args:
            data (str): String no formato "comando arg1 arg2 arg3 ..."
        
        Returns:
            float: Resultado da operação aritmética.
            str: Mensagem de erro se:
                - Comando desconhecido
                - Nenhum argumento fornecido
                - Divisão por zero (para div)
                - Erro no parsing dos argumentos
        
        Note:
            Aceita argumentos decimais (float).
            Requer pelo menos um argumento numérico.
    """
    try:
        parts = data.strip().split()
        
        cmd = parts[0]
        args = parts[1:]  

        if cmd == OperationsEnum.SUM.value:
            if not args:
                return 'Erro: A operação requer pelo menos um número'
            
            nums = [float(a) for a in args]
            return sum(nums)
    
        elif cmd == OperationsEnum.SUB.value:
            if not args:
                return 'Erro: A operação requer pelo menos um número'
            
            nums = [float(a) for a in args]
            total = nums[0]
            for i in nums[1:]:
                total -= i
            return total

        elif cmd == OperationsEnum.PROD.value:
            if not args:
                return 'Erro: A operação requer pelo menos um número'

            nums = [float(a) for a in args]
            total = nums[0]
            for i in nums[1:]:
                total *= i
            return total
        elif cmd == OperationsEnum.DIV.value:
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
        else:
            return '\nErro: Comando desconhecido!\n'
    except:
        return 'Erro'

def number_theory(data):
    """
        Executa operações de teoria dos números (fatorial e primalidade).
        
        Processa comandos relacionados a propriedades numéricas:
        - fat: calcula o fatorial de um número
        - prim: verifica se múltiplos números são primos (paralelo)
        
        Args:
            data (str): String no formato "comando arg1 arg2 ..."
        
        Returns:
            int: Fatorial do número (para comando 'fat').
            list[bool]: Lista de resultados booleanos (para comando 'prim').
            str: Mensagem de erro se:
                - Comando desconhecido
                - Fatorial de número negativo
                - Erro no parsing dos argumentos
        
        Note:
            Usa multiprocessing com pool de 4 processos para 'prim'.
            Suporta fatoriais muito grandes (até 1.000.000 dígitos).
    """
    try:
        parts = data.strip().split()
        
        cmd = parts[0]
        args = parts[1:]  
        if cmd == OperationsEnum.FAT.value:
            num = int(args[0])
            if num < 0:
                return "Erro: fatorial não é definido para números negativos"
            return math.factorial(num)
        elif cmd == OperationsEnum.PRIM.value:
            numbers_list = [int(i) for i in args]

            with multiprocessing.Pool(processes=4) as pool:
                result = pool.map(check_primes, numbers_list)

            return result
        else:
            return '\nErro: Comando desconhecido!\n'
    except:
        return 'Erro'