

class conjunto:
    """ Conjuntos de inteiros em ordem não-decrescente.
        Essa classe permite o armazenamento de conjuntos
        de valores inteiros em uma lista estática com
        tamanho máximo definido na criação do objeto.
    """
    def __init__(self,TAM_MAX):
        """ Construtor: aloca espaço para uma lista de tamanho TAM_MAX
            e inicializa essa lista com zeros. O conjunto representado
            usa apenas as posições entre 0 e self.tamanho-1
        """
        self.elementos = [ 0 ] * TAM_MAX # cria lista estática com 0's
        self.tamanho = 0 # inicializa o conjunto como vazio

    def __str__(self):
        """ devolve a string correspondente ao trecho usado do vetor
        """
        return str(self.elementos[:self.tamanho])
    
    def buscabinaria(self,x):
        """ Busca x no conjunto ordenado por bisecção sucessiva
        """
        inicio = 0 # começa olhando para o vetor todo
        fim = self.tamanho-1
        while fim-inicio+1>0: # enquanto o trecho de busca for não-vazio
            meio = (inicio+fim)//2 # define um índice intermediário
            if x==self.elementos[meio]: # se encontrou x, devolve índice
                return meio
            elif x>self.elementos[meio]: # se x está à direita, corta metade esquerda
                inicio = meio+1
            else: # se x está à esquerda, corta metade direita
                fim = meio-1
        return -1 # se não encontrou


    def uniao(self,B):
        """ Produz a união dos conjuntos self e B por intercalação
        """
        C = conjunto(100) # precisa definir algum tamanho máximo
        i = j = k = 0 # inicializa índices
        # enquanto há elementos nos 2 conjuntos
        while i<self.tamanho and j<B.tamanho:
            # 1º caso: transfere o elemento v[i] de A
            if self.elementos[i]<B.elementos[j]:
                C.elementos[k] = self.elementos[i]
                i += 1
            # 2º caso: transfere o elemento v[j] de B
            elif self.elementos[i]>B.elementos[j]:
                C.elementos[k] = B.elementos[j]
                j += 1
            # 3º caso: há um empate, transfere ambos v[i] e v[j] (de A e B)
            else:
                C.elementos[k] = self.elementos[i]
                i += 1
                j += 1
            # avança índice do conjunto C
            k += 1
        while i<self.tamanho: # se sobraram elementos em A...
            C.elementos[k] = self.elementos[i]
            i += 1
            k += 1
        while j<B.tamanho: # se sobraram elementos em B...
            C.elementos[k] = B.elementos[j]
            j += 1
            k += 1
        C.tamanho = k
        return C



    def interseccao(self,B):
        """ Produz a intersecção dos conjuntos A=self e B.
            O método é parecido com o da união, mas
            só transfere os elementos em caso de "empate".
        """
        C = conjunto(100)
        i = j = k = 0
        while i<self.tamanho and j<B.tamanho:
            if self.elementos[i]<B.elementos[j]:
                i += 1
            elif self.elementos[i]>B.elementos[j]:
                j += 1
            else:
                C.elementos[k] = self.elementos[i]
                i += 1
                j += 1
                k += 1
        C.tamanho = k
        return C
        
        

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
            # procura o lugar certo de elem na lista
            i = 0
            while i<self.tamanho and self.elementos[i]<elem:
                i += 1
            # se elem já existe ou não cabe + ninguém, sai
            if self.elementos[i]==elem or i>=len(self.elementos):
                return
            # encontra terminador
            j = self.tamanho
            # abre espaço para inserir elem na posição i
            while j>=i:
                self.elementos[j+1] = self.elementos[j]
                j -= 1
            # insere elem e atualiza tamanho
            self.elementos[i] = elem
            self.tamanho += 1
        else:
            # chama self.insere(k) para cada k na lista elem.
            for k in elem:
                self.insere(k)

# código de teste
if __name__=="__main__":
    from random import randint
    lista = []
    for i in range(10):
        lista.append(randint(0,20))
    c = conjunto(100) # pode armazenar conjuntos de até 100 elementos
    c.insere(lista)
    print("Conjunto c:")
    print(c)
    lista = []
    for i in range(10):
        lista.append(randint(0,20))
    d = conjunto(100) # pode armazenar conjuntos de até 100 elementos
    d.insere(lista)
    print("Conjunto d:")
    print(d)
    print("União de c e d")
    print(c.uniao(d))
    print("Intersecção de c e d")
    print(c.interseccao(d))
