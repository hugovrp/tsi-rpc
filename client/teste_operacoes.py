import os
import ast
import sys
from operations import Operations

op = Operations()

numeros = list(range(100000))

print(op.prim(*numeros))

'''
print(op.sum(5,2,2,2,2,2,2))
print(op.sum(5,2,2,2,2,2,2))
print(op.prod(0,2,2,2))
print(op.fat(10))
print(op.sub(5,2,2,2))
print(op.div(0,2,2,2))


news = op.news()

if isinstance(news, list):
    print("\nÚltimas notícias do UOL:")
    for i, n in enumerate(news, start=1):
        print(f"{i}. {n}")
else:
    print("Erro ou resposta inesperada:", news)
'''