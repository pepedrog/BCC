
# usado para medir o tempo
import time

# instante inicial
antes = time.clock()

# calcula a mala (x,y,z) de volume ótimo satisfazendo
# restrição x+y+z = 115 (cm) e x,y,z inteiros positivos
vol = 1
xmax = ymax = zmax = 1

# versão mais eficiente: elimina o laço do z forçando
# o obedecimento da condição x+y+z=115, e define ordem
# dos valores (x<=y<=z) para eliminar configurações
# duplicadas.

# percorre valores de x=1,...,113 (afinal y,z>=1)
x = 1
while x<=113:
    # percorre valores de y=x,...,114-x (afinal y>=x e z>=1)
    y = x
    while y<=114-x:
        z = 115-x-y # z já está determinado!
        # testa se a mala (x,y,z) possui maior volume
        if x*y*z>vol:
            vol = x*y*z
            xmax = x
            ymax = y
            zmax = z
        y += 1
    x += 1

# mede o tempo quando acabou a busca
depois = time.clock()

print("As dimensões ótimas são (",xmax,",",ymax,",",zmax,") com volume ",vol," cm3",sep="")
print("Tempo de execução = ",depois-antes," segundos",sep="")
