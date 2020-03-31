
# traz a função imprimematriz do arquivo imprimematriz.py
from imprimematriz import imprimematriz

def multiplicamatrizvetor(A,x):
    """ multiplica a matriz A e o vetor x, se
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
    if len(x)!=ncolunasA:
        return []
    # y = A*x terá dimensão nlinhasA
    y = [ 0 ]*nlinhasA
    for i in range(nlinhasA):
        for j in range(ncolunasA):
            y[i] += A[i][j]*x[j]
    return y
    
# código de teste
if __name__ == "__main__":
    A = [ [ 0, 1, 2 ], [10,11,12], [20,21,22] ]
    print("A")
    imprimematriz(A)
    print("")
    print("x")
    x = [-2, 3, 5]
    print(x)
    print("")
    print("y=A*x")
    y = multiplicamatrizvetor(A,x)
    print(y)
    print("")
