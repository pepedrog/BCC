

def razaoaurea(N):
    """ Computa a melhor aproximação para a razão áurea
        usando inteiros a/b com a,b=1,2,...,N. Não por
        acaso, as soluções envolvem termos consecutivos
        da série de Fibonacci!
    """
    # a razão áurea é definida pela equação a/b = (a+b)/a.
    # queremos o par (a,b) que tenha a menor discrepância
    # entre essas duas expressões.
    
    # melhoraprox = melhora/melhorb
    melhoraprox = 1
    melhora = melhorb = 1

    # procura entre os a=1,...,N
    for a in range(1,N+1):
        # como a+b>a, só faz sentido procurar b=1,...,a.
        # você consegue estimar a economia em relação
        # a buscar b entre 1,...,N?
        for b in range(1,a+1):
            if abs(a/b-(a+b)/a) < melhoraprox:
                melhoraprox = abs(a/b-(a+b)/a)
                melhora, melhorb = a, b
    # devolve o melhor par (a,b) 
    return melhora,melhorb

# busca as aproximações com N = 2**k
for k in range(20):
    N=2**k
    a,b = razaoaurea(N)
    print("a melhor aproximação com N=",N," é ",a,"/",b,"=",a/b)
