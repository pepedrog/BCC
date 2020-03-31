
# traz a função imprimematriz do arquivo imprimematriz.py
from imprimematriz import imprimematriz

def somamatrizes(A,B):
    """ soma as matrizes A e B se
        for possível, senão devolve
        uma matriz vazia.
    """
    nlinhas = len(A)
    # trata matriz com 0 linhas
    if nlinhas>0:
        ncolunas = len(A[0])
    else:
        return []
    # testa se as matrizes têm dimensões compatíveis
    if len(B)==0 or len(B)!=nlinhas or len(B[0])!=ncolunas:
        return []
    # versão 0: ESSA NÃO FUNCIONA!!
    #C = [ [0]*ncolunas ]*nlinhas
    # o problema aqui é que todas as
    # linhas da matriz residem no mesmo
    # lugar: "C[0] is C[1]" retorna True.
    # versão 1: inicializa matriz C com 0's
    #C = []
    #for i in range(nlinhas):
    #    C.append([0]*ncolunas)
    # versão 2: inicializa matriz C com uma cópia de A
    C = []
    for i in range(nlinhas):
        C.append(A[i].copy())
    # soma os elementos em uma varredura por linhas
    for i in range(nlinhas):
        for j in range(ncolunas):
            # versão 1: 
            #C[i][j] = A[i][j] + B[i][j]
            # versão 2:
            C[i][j] += B[i][j]
    return C

# código de teste
if __name__ == "__main__":
    A = [ [ 0, 1, 2 ], [10,11,12], [20,21,22] ]
    print("A")
    imprimematriz(A)
    print("")
    print("B")
    B = [ [ -2, 3, 5], [0, 0, 1], [1, 0 ,-3]  ]
    imprimematriz(B)
    print("")
    print("A+B")
    C = somamatrizes(A,B)
    imprimematriz(C)
    print("")
