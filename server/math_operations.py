import os
import sys
import math
import multiprocessing

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.enums import Math_Enum

sys.set_int_max_str_digits(1000000)

def _is_prime(n):
    if n < 2:
        return False
    
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def check_primes(number):
    return _is_prime(number)

def math_operations(data):
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

