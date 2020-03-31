

# Exercício sugerido na aula de 7/6:
# implementar uma classe que permita o armazenamento de
# conjuntos de valores inteiros em uma lista estática
# com tamanho máximo definido na criação do objeto.
# Veja o exercício 3 da prova 2 para lembrar do contexto.

class conjunto: # conjuntos de inteiros em ordem não-decrescente

    def __init__(self,TAM_MAXIMO):
        """ Construtor: aloca espaço para uma lista de tamanho TAM_MAXIMO
            e inicializa essa lista com zeros. O conjunto representado
            usa apenas as posições entre 0 e self.tamanho-1
        """
        self.elementos = [ 0 ] * TAM_MAXIMO # cria lista estática com 0's
        self.tamanho = 0 # inicializa o conjunto como vazio

    
    def insere(self,elem):
        """ Insere elemento(s) no conjunto, preservando a ordem.
            Se elem for um único inteiro, insere-o na posição
            correta (respeitando a ordem não-decrescente).
            Se elem for uma lista, insere cada elemento no conjunto, um por vez.
        """
        # só tratamos os dois casos acima
        assert type(elem)==int or type(elem)==list
        # primeiro caso:
        if type(elem)==int:
            # adaptação da questão 3a da P2. A principal diferença é
            # que aqui não existe o terminador -1, mas o atributo
            # self.tamanho é quem determina qual é a porção da lista
            # realmente utilizada pelos elementos do conjunto.
            return
        else:
            # adaptação da questão 3b. Se quiser, use a função do
            # item (a), que deve ser chamada como self.insere(k)
            # para cada k na lista elem.
            return

# código de teste
if __name__=="__main__":
    from random import randint
    lista = []
    for i in range(10):
        lista.append(randint(0,1000))
    print("Lista desordenada:")
    print(lista)
    c = conjunto(100) # pode armazenar conjuntos de até 100 elementos
    c.insere(lista)
    print("Conjunto ordenado:")
    print(c)
    
