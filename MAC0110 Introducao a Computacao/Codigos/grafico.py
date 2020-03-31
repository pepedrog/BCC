
def grafico(X,Y,N,condição):
    """ Gera uma imagem percorrendo o retângulo [-X,X]x[-Y,Y]
        discretizado com densidade de N pontos por unidade,
        e testando uma condição para cada par (x,y) percorrido.
        A imagem possui '*'s nos pares (x,y) que satisfazem a
        condição, e ' ' caso contrário.
    """

    # o laço externo percorre os valores de Y em ordem
    # descendente, pois é assim que o gráfico será
    # produzido na tela.
    y = Y
    while y>=-Y:

        # o laço interno percorre os valores de X em
        # ordem crescente, pois serão impressos da
        # esquerda para a direita
        x = -X
        while x<=X:
            
            # testa a condição (armazenada em uma string)
            # para decidir se (x,y) pertence ou não à imagem
            if eval(condição): print("*",end="")
            else: print(" ",end="")
            
            x = x+1/N

        # pula a linha para o próximo valor de y
        print("")
        y = y-1/N

# Para testar a função, diminua a fonte do terminal para
# um tamanho bem pequeno, e use uma densidade >= 50

# esse 1.7 é "gambiarra" para corrigir o aspecto da figura,
# mas depende da fonte, corrija se precisar
a=1.7
grafico(1.5,1.5,100,"x**2+(a*y)**2<1")
grafico(1.5,1.5,100,"0.5<x**2+(a*y)**2<1")
grafico(1.5,1.5,100,"abs((a*y)-x**2)<0.01")
grafico(1.5,1.5,100,"abs((a*y)-x**3+x)<0.01")
grafico(1.5,1.5,100,"abs(x*a*y)*abs(x-a*y)*abs(x+a*y)<0.001")
grafico(1.5,1.5,100,"abs(x-a*y)%0.2<0.01")
grafico(1.5,0.8,100,"(x**2+(a*y)**2-1)**3-x**2*(a*y)**3<0")

