
""" Outro exemplo de uso não tão interessante de recursão: Busca Binária
    Esse é um algoritmo de divisão-e-conquista em que a cada passo usa-se
    um teste de ordem para restringir a busca a uma das metades do vetor.
    O custo computacional é O(log N), o mesmo da implementação direta,
    mas o gasto de memória da implementação recursiva é O(log N)
    (por causa da pilha de chamadas recursivas), ao passo que a versão
    simples usa memória constante.
"""

def buscabinaria(x,v,i,j):
    """ Busca o elemento x no vetor ordenado v, entre os índices i e j-1
    """
    if j-i<=0: # se o trecho do vetor tem menos de 1 elemento, não encontra
        return -1
    m = (i+j)//2 # calcula o índice intermediário
    if x==v[m]: # se encontrou, devolve índice
        return m
    elif x<v[m]: # se x está na metade esquerda, busca lá
        return buscabinaria(x,v,i,m)
    else: # senão, busca na metade direita
        return buscabinaria(x,v,m+1,j)

from random import randint
# cria um vetor aleatório e ordena
l=[]
for i in range(20):
    l.append(randint(0,1000))
l.sort()
print("vetor = ",l)
# busca vários elementos aleatórios
encontrados = []
naoencontrados = []
for i in range(1000):
    x = randint(0,1000)
    if buscabinaria(x,l,0,len(l))==-1:
        if x not in naoencontrados:
            naoencontrados.append(x)
    elif x not in encontrados:
        encontrados.append(x)
encontrados.sort()
naoencontrados.sort()
print("encontrados:",encontrados)
print("não encontrados:",naoencontrados)




    
