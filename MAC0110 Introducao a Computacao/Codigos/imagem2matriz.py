
""" Define as funções de leitura de imagens PGM para uma matriz em Python
    e escrita de matrizes em arquivos de imagem PGM. Os arquivos de entrada
    devem ter o formato

    P2
    <largura> <altura>
    <valor máximo>
    <valores dos pixels entre 0 e 255> ...

    caso queira usar um arquivo que possui linhas com comentários, será
    necessário removê-los (num editor de texto).
"""

if __name__=='__main__':
    print("""
    Define as funções de leitura de imagens PGM para uma matriz em Python
    e escrita de matrizes em arquivos de imagem PGM. Os arquivos de entrada
    devem ter o formato

    P2
    <largura> <altura>
    <valor máximo>
    <valores dos pixels entre 0 e 255> ...

    caso queira usar um arquivo que possui linhas com comentários, será
    necessário removê-los (num editor de texto).
    """)
    exit()


def pgm2matriz(nomedoarquivo):
    """ Lê um arquivo em formato PGM e devolve a matriz correspondente
        aos pixels da imagem em níveis de cinza. Só funciona para
        arquivos com o formato "P2 <largura> <altura> <limite> pixels..."
        sem comentários no meio do arquivo.
    """
    # traz o conteúdo do arquivo para a memória
    # (isso poderia ser feito de forma mais inteligente,
    # lendo o arquivo aos poucos)
    arquivo = open(nomedoarquivo)
    conteudo = arquivo.read()
    arquivo.close()
    lista = conteudo.split()
    # cria matriz M por N com valores do arquivo
    M,N = int(lista[2]), int(lista[1])
    matriz = []
    for i in range(M):
        matriz.append([])
        for j in range(N):
            matriz[i].append(int(lista[4+i*N+j]))
    return matriz

def matriz2pgm(matriz,nomedoarquivo):
    """ Escreve uma matriz como arquivo em formato PGM.
    """
    arquivo = open(nomedoarquivo,"w")
    M,N = len(matriz), len(matriz[0])
    # encontra maior elemento da matriz
    lim = max(matriz[0])
    for i in range(1,M):
        lim = max(lim,max(matriz[i]))
    # escreve cabeçalho
    arquivo.write("P2\n"+str(N)+" "+str(M)+"\n"+str(lim)+"\n")
    # escreve pixels
    for i in range(M):
        for j in range(N):
            arquivo.write(str(matriz[i][j])+" ")
        arquivo.write("\n")
    arquivo.close()

