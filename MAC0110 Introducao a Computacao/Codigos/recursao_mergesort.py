
""" Exemplo de algoritmo recursivo de ordenação: MergeSort
    Ele se baseia na função intercala, que havíamos implementado
    para a união de conjuntos representados em listas ordenadas.
"""

def intercala(v,a,b,c):
    """ Intercala os conjuntos A = { v[i] | a<=i<b }
        e B = { v[j] | b<=j<c }, copiando os valores
        para um vetor w temporário, e depois
        transferindo-os de volta para v.
    """
    w = v.copy() # cria uma cópia de v
    i,j,k = a,b,a # inicializa índices
    while i<b and j<c: # enquanto há elementos nos 2 conjuntos
        if v[i]<v[j]: # transfere o elemento v[i] de A
            w[k] = v[i]
            i += 1
        elif v[i]>v[j]: # transfere o elemento v[j] de B
            w[k] = v[j]
            j += 1
        else: # há um empate, transfere ambos v[i] e v[j] (de A e B)
            w[k] = v[i]
            i += 1
            j += 1
        k += 1
    while i<b: # se sobraram elementos em A...
        w[k] = v[i]
        i += 1
        k += 1
    while j<c: # se sobraram elementos em B...
        w[k] = v[j]
        j += 1
        k += 1
    for i in range(a,c): # copia sequência intercalada de volta para v
        v[i] = w[i]

def mergesort(v,inicio,fim):
    """ Algoritmo de ordenação por intercalação recursiva: a ideia
        é simples: se o vetor v tem 0 ou 1 elementos, ele já está
        ordenado (essa é a base da recursão); do contrário, ordena-se
        recursivamente as duas metades e intercala-se os resultados.
    """
    if fim-inicio<=1: return # caso em que |v| = 0 ou 1
    meio = (inicio+fim)//2 # corta o vetor ao meio
    mergesort(v,inicio,meio) # ordena a primeira metade
    mergesort(v,meio,fim) # ordena a segunda metade
    intercala(v,inicio,meio,fim) # intercala as metades
    
from random import randint
# cria um vetor aleatório e ordena
l=[]
for i in range(20):
    l.append(randint(0,1000))
print("vetor original =",l)
mergesort(l,0,len(l))
print("vetor ordenado =",l)
