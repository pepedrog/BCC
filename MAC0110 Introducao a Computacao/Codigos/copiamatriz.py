
""" Define uma função que copia os valores de uma matriz em
    uma nova matriz (sem copiar referências das linhas).
"""

def copiamatriz(A):
    """ Produz uma cópia da matriz A.
    """
    B = []
    for linha in A:
        B.append(linha.copy())
    return B

