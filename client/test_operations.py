import os
import ast
import sys
from client.operations import Operations

op = Operations()

""" Teste Servidor 1

print(op.prod(0,2,2,2))
print(op.sub(5,2,2,2))
print(op.div(0,2,2,2))
print(op.sum(5,2,2,2,2,2,2))
"""



""" Teste Servidor 2

print(op.fat())

numeros = list(range(10))

print(op.prim(*numeros))
"""



""" Teste Servidor 3

news = op.news()

if isinstance(news, list):
    print("\nÚltimas notícias do UOL:")
    for i, n in enumerate(news, start=1):
        print(f"{i}. {n}")
else:
    print("Erro ou resposta inesperada:", news)
"""

print(op.solver("Calcule a raiz quadrada de 25"))