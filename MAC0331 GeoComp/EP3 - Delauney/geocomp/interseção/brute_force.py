from geocomp.common import prim
from geocomp.common import segment
from geocomp.common.control import sleep
from geocomp import config

def Brute_force (l):
    "Algoritmo força bruta para encontrar todos as interseções entre uma lista de segmentos"

    for s in l:
        s.plot()

    for i in range(0, len(l) - 1):
        l[i].plot("blue")
        sleep()
        for j in range(i + 1, len(l)):
            l[j].plot("cyan")
            sleep()
            if (l[i].intersects(l[j])):
                l[i].hide()
                l[j].hide()
                l[i].plot("yellow")
                l[j].plot("yellow")
                inter = l[i].intersection(l[j])
                inter.hilight("yellow")
                sleep()
                l[i].hide()
                l[j].hide()
                l[i].plot("blue")
            l[j].hide()
        l[i].hide()
