
def invertestring(s):
    """ Inverte as letras da string s
    """
    inv = ""
    for i in range(len(s)):
        inv = inv+s[-i-1]
    return inv


def invertelista(l):
    """ Função que recebe uma lista l e devolve outra lista,
        com os mesmos elementos na ordem inversa.
    """
    inv = []
    for i in range(len(l)):
        inv.append(l[-i-1])
    return inv

frase = input("Digite uma frase: ")
print("A frase invertida é: ")
print(invertestring(frase))
lista = frase.split() # gera uma lista com cada palavra da frase
listainvertida = invertelista(lista)
print("A lista invertida de palavras invertidas é: ")
for i in range(len(lista)):
    print(invertestring(listainvertida[i]))
