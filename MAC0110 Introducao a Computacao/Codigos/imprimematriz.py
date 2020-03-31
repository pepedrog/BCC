
def imprimematriz(A):
    """ imprime a matriz A na tela
        em formato tabular.
    """
    nlinhas = len(A)
    # se a matriz é vazia não imprime nada.
    if nlinhas>0:
        ncolunas = len(A[0])
    else:
        return
    # faz a varredura da matriz por linhas
    for i in range(nlinhas):
        for j in range(ncolunas):
            print(A[i][j],end="\t")
        print("")

# esse if faz com que o código de teste
# a seguir só seja executado quando esse
# arquivo for executado como programa
# principal pelo interpretador Python.
# isso será útil para os exemplos
# somamatrizes e multiplicamatrizes.
if __name__ == "__main__":
    A = [ [ 0, 1, 2 ], [10,11,12], [20,21,22] ]
    print("A")
    imprimematriz(A)
    print("")
    print("B")
    B = [ [ -2, 3, 5], [0, 0, 1], [1, 0 ,-3]  ]
    imprimematriz(B)
    print("")
