
# usado para medir o tempo
import time

# instante inicial
antes = time.clock()

# calcula a mala (x,y,z) de volume ótimo satisfazendo
# restrição x+y+z = 115 (cm) e x,y,z inteiros positivos
vol = 1
xmax = ymax = zmax = 1

# versão um pouco mais eficiente: restringe valores
# de x,y,z conforme os outros valores. Você consegue
# estimar quanto de economia isso representa?

# percorre valores de x=1,...,113 (pois y,z>=1)
x = 1
while x<=113:
    # percorre valores de y=1,...,114-x (pois z>=1)
    y = 1
    while y<=114-x:
        z = 1
        # percorre valores de z=1,...,115-x-y
        while z<=115-x-y:
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
