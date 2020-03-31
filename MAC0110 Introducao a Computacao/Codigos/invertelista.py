
def invertelista(l):
    """ Função que recebe uma lista l e devolve outra lista,
        com os mesmos elementos na ordem inversa.
    """
    inv = []
    for i in range(len(l)):
        inv.append(l[-i-1])
    return inv

N = int(input("Digite o tamanho da lista: "))
lista = []
for i in range(N):
    lista.append(int(input("Digite um elemento da lista: ")))
listainvertida = invertelista(lista)
print("A lista invertida é: ")
for i in range(N):
    print(listainvertida[i])
