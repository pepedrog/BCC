
class matriz:
    """ Classe de matrizes: permite o uso natural de expressões
        algébricas envolvendo somas e produtos de matrizes.

        As matrizes dessa classe possuem 3 atributos:
            nlin = número de linhas
            ncol = número de colunas
            val = lista de listas usadas para armazenar as entradas numéricas

        A classe permite criar uma nova matriz de 3 jeitos:
            m = matriz(M,N) # cria uma matriz de tamanho MxN com zeros
            m = matriz(A) # onde A é uma matriz Python (lista de listas) usada para inicializar o objeto
            m = matriz(A) # onde A é um objeto da classe matriz, cria uma cópia

        Os métodos mágicos implementados permitem
            - operações de soma, subtração e multiplicação de matrizes
            - operação de indexação, usando a notação A[i] para acessar uma linha inteira,
                                     ou A[i,j] para acessar o elemento na posição (i,j)
    """


    # método construtor
    
    
    def __init__(self,x,y=-1):
        """ construtor: permite criar um objeto matriz passando como argumentos:
                        opção 1: as dimensões M,N da matriz (cria uma matriz com zeros)
                        opção 2: uma lista de listas (representação padrão Python para matrizes)
                        opção 3: um objeto matriz a ser clonado
        """

        # verifica algumas condições básicas sobre os argumentos nas 3 opções acima
        assert (type(x)==int and type(y)==int and x>0 and y>0) \
               or \
               (type(x)==list and len(x)>0 and type(x[0])==list and len(x[0])>0) \
               or \
               type(x)==matriz
        # na opção 1, usa função auxiliar redimensiona para criar matriz de zeros
        if type(x)==int:
            self.redimensiona(x,y)
        # na opção 2, cria matriz de zeros e transfere (clona) o conteúdo da lista de listas
        elif type(x)==list: # x é uma matriz
            self.redimensiona(len(x),len(x[0]))
            self.transfere(x)
        # na opção 3, cria matriz de zeros e transfere o conteúdo do objeto matriz passado como argumento
        else:
            self.redimensiona(x.nlin,x.ncol)
            self.transfere(x.val)


    # método de impressão
            

    def __str__(self):
        """ imprime a matriz na tela em formato tabular.
        """
        saida = ""
        # faz a varredura da matriz por linhas
        for i in range(self.nlin):
            for j in range(self.ncol):
                saida += str(self.val[i][j])+"\t"
            saida += "\n"
        return saida[0:-1] # tira o último "\n"


    # métodos algébricos
    
    
    def __add__(self,B):
        """ método A+B: soma as matrizes A=self e B (se for possível)
        """
        # testa se as matrizes têm dimensões compatíveis
        assert self.nlin==B.nlin and self.ncol==B.ncol
        # inicializa matriz C com uma cópia de A
        C = matriz(self.val)
        # soma os elementos de B em uma varredura por linhas
        for i in range(self.nlin):
            for j in range(self.ncol):
                C.val[i][j] += B.val[i][j]
        return C


    def __sub__(self,B):
        """ método A-B: subtrai da matriz A=self a matriz B (se for possível)
        """
        # testa se as matrizes têm dimensões compatíveis
        assert self.nlin==B.nlin and self.ncol==B.ncol
        # inicializa matriz C com uma cópia de A
        C = matriz(self.val)
        # soma os elementos de B em uma varredura por linhas
        for i in range(self.nlin):
            for j in range(self.ncol):
                C.val[i][j] -= B.val[i][j]
        return C


    def __mul__(self,B):
        """ método A*B: multiplica as matrizes A=self e B (se for possível)
        """
        # testa se as matrizes A e B são compatíveis
        assert self.ncol==B.nlin
        # a nova matriz C=A*B terá dimensões A.nlin x B.ncol
        C = matriz(self.nlin,B.ncol)
        # percorre a matriz C por linhas: cada elemento C[i][j] é a soma,
        # para k=0,1,...,B.ncol-1 dos valores A[i][k]*B[k][j]    
        for i in range(self.nlin):
            for j in range(B.ncol):
                for k in range(self.ncol):
                    C.val[i][j] += self.val[i][k]*B.val[k][j]
        return C


    # métodos de acesso direto a índices da matriz
    
    
    def __getitem__(self,k):
        """ método de acesso a A[i] ou A[i][j]: permite o acesso "natural" ao conteúdo
            da matriz, dispensando o acesso indireto através do atributo val.
        """
        return self.val[k]


    def __setitem__(self,k,val):
        """ método de atribuição a A[i]: permite a manipulação de linhas
            inteiras ou elementos individuais usando uma notação mais compacta.
        """
        self.val[k] = val.copy()


    # funções auxiliares usadas pelo construtor

    
    def redimensiona(self,nlin,ncol):
        """ método redimensiona: aloca espaço de tamanho nlin x ncol
            para a matriz, e inicializa todos as entradas com zeros.
        """
        self.nlin = nlin
        self.ncol = ncol
        self.val = []
        for i in range(nlin):
            self.val.append([])
            for j in range(ncol):
                self.val[i].append(0)

    def transfere(self,A):
        """ método transfere: copia o conteúdo de uma matriz em
            formato Python nativo (lista de listas) para o objeto.
        """
        assert self.nlin==len(A) \
            and self.ncol==len(A[0])
        for i in range(self.nlin):
            for j in range(self.ncol):
                self.val[i][j] = A[i][j]
                


# códigos de teste
                
if __name__=="__main__":
    m = matriz([[1,2,3],[4,5,6],[7,8,9]])
    print("m=",m,sep="\n")
    n = matriz([[0,1,-1],[-1,0,1],[1,-1,0]])
    print("n=",n,sep="\n")
    p = m+n # equivalente a m.__add__(n), mais fácil que m.somamatriz(n)
    print("m+n=",p,sep="\n")
    q = m-n # equivalente a m.__sub__(n), mais fácil que m.subtraimatriz(n)
    print("m-n=",q,sep="\n")
    r = m*n # equivalente a m.__mul__(n), mais fácil que m.multiplicamatriz(n)
    print("m*n=",r,sep="\n")
    print("acesso direto: m[0][0] =",m[0][0]) # equivalente a m.__getitem__(0)[0], mais fácil que m.val[0][0]
    m[0][0] = -1 # equivalente a m.__getitem__(0)[0] = -1, mais fácil que m.val[0][0] = -1
    print("alteração direta: m[0][0] =",m[0][0])
    m[0] = n[0] # equivalente a m.__setitem__(0) = n.__getitem__(0).copy(),
                # mais fácil que m.val[0] = n.val[0].copy()
    print("copiando primeira linha de n em m (m[0] = n[0]):")
    print("m=",m,sep="\n")
