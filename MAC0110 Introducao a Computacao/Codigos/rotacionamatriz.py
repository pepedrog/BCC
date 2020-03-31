
"""
Esse exemplo mostra como fazer rotações de elementos armazenados em
uma matriz. Além de possuir interesse teórico/geométrico, uma aplicação
desse problema corresponde à rotação de imagens, que veremos em um
exemplo subsequente. A ideia é simples: cada índice (i,j) será mapeado
em um vetor (xij,yij) em um sistema de coordenadas xy posicionado no
centro da matriz, e esse vetor (xij,yij) será rotacionado em w graus
no sentido anti-horário para definir o vetor (xkl,ykl) correspondente
à posição B[k][l] onde o elemento A[i][j] deve ser mapeado.
A figura abaixo ilustra isso: o centro da matriz está indicado por um '+',
as posições (i,j) e (k,l) (índices da matriz) estão indicados com '*'s e
os vetores (xij,yij) e (xkl,ykl), separados por um ângulo w, estão
indicados pelas barras inclinadas:

+---------------------+ 
|                     | 
|                     | Na nova matriz B 
|                     | teremos que colocar
|    (k,l)   (i,j)    | o valor A[i][j] na 
|      *       *      | posição B[k][l].
|       \  w  /       | 
|  [xkl] \___/ [xij]  | 
|  [ykl]  \ /  [yij]  | Alternativamente, 
|          +          | poderíamos obter
|                     | (i,j) a partir de 
|                     | (k,l) por uma
|                     | rotação de -w graus, 
|                     | e isso é o
|                     | que será feito
|                     | na implementação
|                     | abaixo.
|                     | 
+---------------------+ 
"""

# traz funções/valores da biblioteca math
from math import sin,cos,pi
# a função imprimematriz foi implementada em aula (e está no PACA)
from imprimematriz import imprimematriz
# a função multiplicamatrizvetor é uma variação simples
# da multiplicamatrizes (e também está no PACA)
from multiplicamatrizvetor import multiplicamatrizvetor

# Observação: o código abaixo foi implementado em aula seguindo
# uma estratégia denominada "top-down", onde primeiro resolvemos
# o problema geral, delegando tarefas para funções auxiliares
# que serão implementadas posteriormente. Note que a ordem das
# funções no código abaixo também reflete isso, e cada função
# chama outras funções que ainda não foram definidas.
# Quiz: por que isso não dá problema?

def rotaciona(A,w):
    """ rotaciona em w graus os elementos de uma matriz A.
    """
    # obtém as dimensões de A
    M = len(A)
    N = len(A[0])
    # inicializa uma matriz B, de mesmo tamanho que A, com zeros
    B = [[]]*M
    for i in range(M):
        B[i] = [0]*N
    # para cada índice (i,j) em B, procura o índice
    # (k,l) correspondente em A fazendo uma rotação
    # de -w graus, assim (k,l) rotacionado em w graus
    # corresponderá ao (i,j).
    for i in range(M):
        for j in range(N):
            k,l = indicerotacionado(i,j,-w,M,N)
            # testa se o índice em A é válido
            # e transfere o conteúdo de A para B.
            if k in range(M) and l in range(N):
                B[i][j] = A[k][l]
    return B

def indicerotacionado(i,j,w,M,N):
    """ rotaciona o índice (i,j) em w graus numa matriz de MxN,
        considerando um sistema de coordenadas xy posicionado em
        (N//2,M//2) (que é o centro da matriz).
    """
    # muda (i,j) para novo sistema de coordenadas xy.
    #
    # a "transposição" (i-->y e j-->x) se deve ao fato
    # de que nas matrizes o primeiro índice é o das
    # linhas, que corresponde ao eixo vertical no plano xy.
    # 
    # a diferença de sinal nos dois eixos se deve ao
    # fato de que as linhas das matrizes são indexadas
    # de cima para baixo, ao contrário do eixo y.
    xij, yij = j-N//2,M//2-i
    # rotaciona (xij,yij) de w graus
    # transforma em radianos para calcular sin/cos
    w = 2*pi*w/360
    # usa a matriz de rotação do plano xy de um ângulo w
    # para entender a matemática da rotação no plano,
    # veja as páginas 25-27 do documento:
    # https://www.essentialmath.com/GDC2012/GDC2012_JMV_Rotations.pdf
    Mrotacao = [[cos(w), -sin(w)],[sin(w), cos(w)]]
    # obtém (xkl,ykl) como rotação de (xij,yij)
    [xkl,ykl] = multiplicamatrizvetor(Mrotacao,[xij,yij])
    # muda (xkl,ykl) para sistema de coordenadas original
    # (lembrando da transposição e inversão do eixo y)
    k,l = round(M//2-ykl),round(N//2+xkl)
    return k,l

# caso seja rodado como programa principal, imprime a documentação
# e chama a função de teste.
if __name__=='__main__':

    print(__doc__) # variável que contém a docstring do módulo
    
    # Função de teste
    def teste():
        A = [[1,2,3],[4,5,6],[7,8,9]]
        for w in range(0,361,45):
            B = rotaciona(A,w)
            print("matriz rotacionada em",w,"graus:")
            imprimematriz(B)
            print()

    teste()
