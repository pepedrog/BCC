'''
   MAC0122 Principios de Desenvolvimneto de algoritmos
 
   hilbert.py
 
   Programa para desenhar curvas de Hilbert,
'''

#--------------------------------------------------
# modulo utilizado desenhar as curvas
import turtle
import random

#--------------------------------------------------
# Constantes
# direçao para movimentos
DIREITA  = 0
ESQUERDA = 1
CIMA     = 2
BAIXO    = 3

# tamanho da janela
LARGURA_JANELA = 1024

# canto inferioe da janela
X_INF = -LARGURA_JANELA//2
Y_INF = -LARGURA_JANELA//2

# canto superior da janela
X_SUP =  LARGURA_JANELA//2
Y_SUP =  LARGURA_JANELA//2

# prompt
PROMPT = "hilbert >>> "

FIM   = "fim"


#---------------------------------------------------
def main():
    '''(None) -> None

    Funçao que le iterativamente valores inteiros e cria
    desenha a curva de Hilbet correspondente.

    O programa pára assim que o string FIM é digitado.
    '''
     
    print("Programa para desenhar curvas de Hilbert")
    
    # crie a janela onde as curvas serão desenhadas. 
    janela = turtle.Screen()

    # cores 
    janela.colormode(255)

    # coordenadas
    janela.setworldcoordinates(X_INF, Y_INF, X_SUP, Y_SUP)

    # delay
    janela.delay(20)
    
    resposta = input(PROMPT)
    while  resposta != FIM:    
        # converte um string representando um inteiro para int
        try:
            k = int(resposta)
            print("desenhando a curva H%d..." %(k))
            hilbert(k)
        # se usuario digitou algo diferente de FIM e int
        # apresente mensagem de erro
        except ValueError:
            help()

        # espere pela opçao do usuario    
        resposta = input(PROMPT)
    
    # para fechar a janela
    janela.bye()
    
#---------------------------------------------------
def hilbert(k):
    '''(int) -> None

    Recebe um inteiro k e desenha a curva de Hilbert
    H_k em uma janela que a funçao supoe ja ter sido
    criada.
    '''
    
    # crie o pincel
    pincel = turtle.Turtle()

    # defina a espessura do pincel
    pincel.pensize(2)

    # defina a cor da tinta
    pincel.color(random.randrange(256),random.randrange(256),\
                 random.randrange(256))

    # defina velocidade do desenho: e bom ser um pouco
    #      lento para vermos o desenho se formando
    pincel.speed(10)
    
    # levante o pincel
    pincel.penup()

    # mova o pincel para a posiçao de inicio da curva
    largura      = LARGURA_JANELA 
    deslocamento = 0
    for i in range(k):
        largura //= 2
        deslocamento += largura//2
            
    #  x, y = pincel.pos() posicao inicial e (0,0)    
    x = deslocamento
    y = deslocamento
    pincel.goto(x,y)
    
    # abaixe o pincel
    pincel.pendown()
    
    a(k,pincel,largura)
    # para fechar a janela basta clicar sobre ela
  
#---------------------------------------------------------
def a(k, pincel, comprimento):
    '''(int, Turtle, int) -> None

    Recebe um inteiro k, um pincel em uma determinada
    posição da janela e um inteiro comprimento. A função
    desenha a curva A_k a partir da posição do pincel. O
    valor comprimento é a medida dos segmentos da curva.

    '''
    if k > 0: 
        d(k-1, pincel, comprimento)
        mova(pincel, ESQUERDA, comprimento)
        a(k-1, pincel, comprimento)
        mova(pincel, BAIXO   , comprimento)
        a(k-1, pincel, comprimento)
        mova(pincel, DIREITA , comprimento)
        b(k-1, pincel, comprimento)

#---------------------------------------------------------
def b(k, pincel, comprimento):
    '''(int, Turtle, int) -> None

    Recebe um inteiro k, um pincel em uma determinada
    posição da janela e um inteiro comprimento. A função
    desenha a curva B_k a partir da posição do pincel. O
    valor comprimento é a medida dos segmentos da curva.
    '''
    if k > 0: 
        c(k-1, pincel, comprimento)
        mova(pincel, CIMA   , comprimento)
        b(k-1, pincel, comprimento)
        mova(pincel, DIREITA, comprimento)
        b(k-1, pincel, comprimento)
        mova(pincel, BAIXO  , comprimento)
        a(k-1, pincel, comprimento)

#---------------------------------------------------------
def c(k, pincel, comprimento):
    '''(int, Turtle, int) -> None

    Recebe um inteiro k, um pincel em uma determinada
    posição da janela e um inteiro comprimento. A função
    desenha a curva C_k a partir da posição do pincel. O
    valor comprimento é a medida dos segmentos da curva.
    '''
    if k > 0:
        b(k-1, pincel, comprimento)
        mova(pincel, DIREITA, comprimento)
        c(k-1, pincel, comprimento)
        mova(pincel, CIMA    , comprimento)
        c(k-1, pincel, comprimento)
        mova(pincel, ESQUERDA, comprimento)
        d(k-1, pincel, comprimento)

#---------------------------------------------------------        
def d(k, pincel, comprimento):
    '''(int, Turtle, int) -> None

    Recebe um inteiro k, um pincel em uma determinada
    posição da janela e um inteiro comprimento. A função
    desenha a curva C_k a partir da posição do pincel. O
    valor comprimento é a medida dos segmentos da curva.
    '''
    if k > 0: 
        a(k-1, pincel, comprimento)
        mova(pincel, BAIXO   , comprimento)
        d(k-1, pincel, comprimento)
        mova(pincel, ESQUERDA, comprimento)
        d(k-1, pincel, comprimento)
        mova(pincel, CIMA    , comprimento)
        c(k-1, pincel, comprimento)

#-----------------------------------------------------
def mova(pincel, direcao, comprimento):
    '''(turtle, int, int) -> None
 
    Recebe um pincel em uma determinada posição, um valor
    direcao e um valor comprimento e traça uma linha
    a partir da posição do pincel na direção dada e do
    comprimento dado.
    '''
    # pegue a posição do pincel
    x, y = pincel.pos()

    # calcule nova posição
    if direcao == DIREITA:
        x = x + comprimento
    elif direcao == ESQUERDA:
        x = x - comprimento
    elif direcao == CIMA:
        y = y + comprimento
    elif direcao == BAIXO:
        y = y - comprimento

    pincel.goto(x,y)

#-----------------------------------------------------
def help():
    '''(None) -> None
    Imprime explicaçao de como usar o programa
    '''
    print("Digite um inteiro k para desenhar a curva Hk ou\n" +
          "       'fim' para encerrar o programa.") 
#-----------------------------------------------------
# chamada da função main()
if __name__ == "__main__":
    main()
