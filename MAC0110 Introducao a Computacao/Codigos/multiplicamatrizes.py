
# traz a função imprimematriz do arquivo imprimematriz.py
from imprimematriz import imprimematriz

def multiplicamatrizes(A,B):
    """ multiplica as matrizes A e B se
        for possível, senão devolve
        uma matriz vazia.
    """
    nlinhasA = len(A)
    # trata matriz com 0 linhas
    if nlinhasA>0:
        ncolunasA = len(A[0])
    else:
        return []
    # testa se as matrizes são compatíveis
    if len(B)!=ncolunasA:
        return []
    ncolunasB = len(B[0])
    # a matriz C=A*B terá dimensões nlinhasA x ncolunasB
    C = []
    # inicializa a matriz C com 0's
    for i in range(nlinhasA):
        C.append([0]*ncolunasB)
    # percorre a matriz C por linhas
    # cada elemento C[i][j] é a soma,
    # para k=0,1,...,ncolunasB-1
    # dos valores A[i][k]*B[k][j]    
    for i in range(nlinhasA):
        for j in range(ncolunasB):
            for k in range(ncolunasA):
                C[i][j] += A[i][k]*B[k][j]
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
    print("A*B")
    C = multiplicamatrizes(A,B)
    imprimematriz(C)
    print("")
