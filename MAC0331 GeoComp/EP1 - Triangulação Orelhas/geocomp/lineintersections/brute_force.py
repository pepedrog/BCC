from geocomp.common import prim
from geocomp.common import segment
from geocomp.common import control
from geocomp import config

def Brute_force (l):
    filter_segments(l)
    intersections = []

    for s in l:
        s.plot()

    for i in range(0, len(l) - 1):
        l[i].hilight(color_line = "blue")
        control.sleep()
        for j in range(i + 1, len(l)):
            l[j].hilight()
            control.sleep()
            if (prim.intersect(l[i].init, l[i].to, l[j].init, l[j].to)):
                # guarda os indices dos segmentos que se intersectam
                l[i].hilight(color_line = "yellow")
                l[j].hilight(color_line = "yellow")
                control.sleep()                
                intersections.append((i, j))
                l[i].hilight(color_line = "blue")
            l[j].plot()
        l[i].plot()

def filter_segments (l):
    for i in range (len(l)):
        if (l[i].init.x > l[i].to.x):
            l[i].init, l[i].to = l[i].to, l[i].init
        elif (l[i].init.x == l[i].to.x):
            if (l[i].init.y > l[i].to.y):
                l[i].init, l[i].to = l[i].to, l[i].init
