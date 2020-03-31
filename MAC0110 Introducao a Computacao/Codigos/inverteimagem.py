
# Esse módulo foi feito para ser rodado como programa principal,
# e inverte o mapa de cores de uma imagem PGM. Use a chamada:
#
# python3 inverteimagem.py <arq-entrada> <ângulo> <arq-saída>

# usamos o módulo sys para acessar os argumentos da linha de comando (sys.argv)
import sys

# verifica se foi chamado como programa principal com o número correto de parâmetros
if __name__!='__main__' or len(sys.argv)!=3:

    print("Use a chamada:\npython3 inverteimagem.py <arq-entrada> <arq-saída>")

else:

    # o módulo imagem2matriz possui as funções de conversão imagem<->matriz<->imagem
    import imagem2matriz
    # o módulo copiamatriz possui uma função para criar cópias "seguras"
    # (sem copiar referências).
    import copiamatriz

    # extrai os parâmetros da linha de comando
    entrada = sys.argv[1]
    saida = sys.argv[2]
    # lê o arquivo PGM de entrada e armazena na matriz A
    A = imagem2matriz.pgm2matriz(entrada)
    # obtém o tamanho e o valor máximo de A
    M,N = len(A),len(A[0])
    maximo = max(A[0])
    for i in range(1,M):
        maximo = max(max(A[i]),maximo)
    # inverte as cores de A
    B = copiamatriz.copiamatriz(A)
    for i in range(M):
        for j in range(N):
            B[i][j] = maximo-A[i][j]
    # escreve a matriz B no arquivo PGM de saída
    imagem2matriz.matriz2pgm(B,saida)

