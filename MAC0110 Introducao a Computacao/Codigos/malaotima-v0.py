
# usado para medir o tempo
import time

# instante inicial
antes = time.clock()

# calcula a mala (x,y,z) de volume ótimo satisfazendo
# restrição x+y+z = 115 (cm) e x,y,z inteiros positivos
vol = 1
xmax = ymax = zmax = 1

# versão mais simplória: percorre todos os valores de x,y,z
# entre 1 e 115, testando a condição e selecionando os
# maiores volumes

# percorre valores de x=1,...,115
x = 1
while x<=115:
    # percorre valores de y=1,...,115
    y = 1
    while y<=115:
        z = 1
        # percorre valores de z=1,...,115
        while z<=115:
            # testa se (x,y,z) satisfaz a restrição
            if x+y+z==115:
                # testa se a mala (x,y,z) possui maior volume
                if x*y*z>vol:
                    vol = x*y*z
                    xmax = x
                    ymax = y
                    zmax = z
            z += 1
        y += 1
    x += 1

# mede o tempo quando acabou a busca
depois = time.clock()

print("As dimensões ótimas são (",xmax,",",ymax,",",zmax,") com volume ",vol," cm3",sep="")
print("Tempo de execução = ",depois-antes," segundos",sep="")
