
# Esse módulo foi feito para ser rodado como programa principal,
# e realiza uma rotação arbitrária em uma imagem PGM. Use a chamada:
#
# python3 entortaimagem.py <arq-entrada> <ângulo> <arq-saída>

# usamos o módulo sys para acessar os argumentos da linha de comando (sys.argv)
import sys

# verifica se foi chamado como programa principal com o número correto de parâmetros
if __name__!='__main__' or len(sys.argv)!=4:

    print("Use a chamada:\npython3 entortaimagem.py <arq-entrada> <ângulo> <arq-saída>")

else:

    # o módulo imagem2matriz possui as funções de conversão imagem<->matriz<->imagem
    import imagem2matriz
    # o módulo rotacionamatriz possui a função rotaciona(matriz,angulo)
    import rotacionamatriz

    # extrai os parâmetros da linha de comando
    entrada = sys.argv[1]
    angulo = sys.argv[2]
    saida = sys.argv[3]
    # lê o arquivo PGM de entrada e armazena na matriz A
    A = imagem2matriz.pgm2matriz(entrada)
    # rotaciona a matriz A de <angulo> graus e armazena em B
    B = rotacionamatriz.rotaciona(A,int(angulo))
    # escreve a matriz B no arquivo PGM de saída
    imagem2matriz.matriz2pgm(B,saida)

