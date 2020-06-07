from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import disc
from geocomp.common.control import sleep
from geocomp import config

def Brute_force (l):
    "Algoritmo força bruta para encontrar todos as interseções entre uma lista de círculos"

    for i in range( len(l)):
        plot_id = l[i].hilight_circ (color = "green", width = 2)
        sleep()
        for j in l[i+1:]:
            j.hilight_circ()
            sleep()
            for p in l[i].intersection(j):
                p.hilight('yellow')
            j.unhilight_circ ()
        l[i].unhilight_circ (plot_id)
    
    
