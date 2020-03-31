
""" Exemplo de péssimo uso de recursão: Fibonacci
    Apesar da definição matemática sugerir uma
    implementação recursiva, o custo da implementação
    abaixo é de fib(n) chamadas da função para
    calcular o valor fib(n) (compare com a implementação
    "simples" usando 3 variáveis, que calcula fib(n)
    com apenas n iterações).
"""

def fib(n):
    if n==0 or n==1:
        return 1
    else:
        return fib(n-1)+fib(n-2)

print("fib(10)=",fib(10))
