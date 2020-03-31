
def pi(R):
    """ Adaptação da função grafico para computar uma
        aproximação de pi pela área de um círculo de raio R.
    """
    # S é a área (igual a pi*R**2)
    S = 0
    
    # o laço externo percorre os valores de Y em ordem descendente
    y = R
    while y>=-R:

        # o laço interno percorre os valores de X em ordem crescente
        x = -R
        while x<=R:
            
            # testa se o ponto (x,y) pertence ao círculo
            if x**2+y**2<=R**2: S += 1
            
            x = x+1

        y = y-1

    # devolve a aproximação de pi = S/R**2
    return S/R**2

# usamos time.clock() para medir o tempo.
# mude o código abaixo para gerar pares
# R    T
# onde R é o raio e T é o tempo em segundos,
# e use o programa graph para visualizar
# essa função.

import time

# percorre valores de R = 2**i
for i in range(20):
    c = time.clock() # mede o tempo antes de calcular o pi
    print("pi(",2**i,")=",pi(2**i),sep="",end="\t\t\t")
    print("tempo =",time.clock()-c,"segundos")
