#!/usr/bin/env python
"""
Algoritmo QuickHull para determinação do fecho convexo
Pedro Gigeck Freire 10737136
"""

from geocomp.common.prim import left, right, area2
from geocomp.common.control import sleep

def particione (P, l, r):

    # P[l + 1] recebe ponto extremo
    for i in range(l + 1, r):
        P[i].lineto(P[l], "gray")
        P[i].lineto(P[r], "gray")
        sleep()
        P[i].remove_lineto(P[l])
        P[i].remove_lineto(P[r])
        if abs(area2(P[i], P[l], P[r])) > abs(area2(P[l + 1], P[l], P[r])):
            P[i], P[l + 1] = P[l + 1], P[i]

    # Desenha o triangulo
    if hasattr(P[l + 1], 'hi'): P[l + 1].unhilight()
    P[l + 1].hilight("firebrick")
    linha_esq = P[l].lineto(P[l + 1], "green")
    linha_dir = P[r].lineto(P[l + 1], "red")
    sleep()
    
    p = q = r
    for k in range(r - 1, l + 1, -1):
        if hasattr(P[k], 'hi'): P[k].unhilight()
        P[k].hilight("yellow")
        sleep()
        P[k].unhilight()
        if left (P[l], P[l + 1], P[k]):
            # ponto da partição esquerda (verde)
            p -= 1
            P[p], P[k] = P[k], P[p]
            P[p].hilight("green")
            sleep()
        elif right (P[r], P[l + 1], P[k]):
            # ponto da partição direita (vermelho)
            p -= 1
            q -= 1
            P[q], P[k] = P[k], P[q]
            if p != q: P[p], P[k] = P[k], P[p]
            P[q].hilight("red")
            sleep()
    
    # Ajustes finais no vetor
    p -= 1
    q -= 1
    P[q], P[l + 1] = P[l + 1], P[q]
    if p != q:
        P[p], P[l + 1] = P[l + 1], P[p]
    p -= 1
    P[l], P[p] = P[p], P[l]

    return p, q, linha_esq, linha_dir

def quickhull_rec (P, l, r):
    if r - l == 1:
        P[l].unhilight()
        P[r].unhilight()
        P[l].lineto(P[r], "orange")
        sleep()
        return [P[r], P[l]]
    
    p, q, linha_esq, linha_dir = particione (P, l, r)
    
    P[p].unhilight()
    P[q].unhilight()
    P[p].hilight("green")
    P[q].hilight("red")
    sleep()

    fecho_esq = quickhull_rec (P, p, q)
    fecho_dir = quickhull_rec (P, q, r)
    
    P[l].remove_lineto(P[q], id = linha_esq)
    P[r].remove_lineto(P[q], id = linha_dir)
    sleep()
    
    for e in range (1, len(fecho_esq)):
        fecho_dir.append (fecho_esq[e])
    
    return fecho_dir

def quickhull (P):
    if len(P) <= 1: return P

    # Ponto mais baixo
    for i in range(len(P)):
        if P[i].y < P[0].y or (P[i].y == P[0].y and P[i].x > P[0].x): 
            P[0], P[i] = P[i], P[0]

    # Ponto mais a direita do ponto mais baixo
    for i in range(len(P)):
        if right (P[0], P[-1], P[i]): P[-1], P[i] = P[i], P[-1]
    
    P[0].hilight("green")
    P[-1].hilight("red")
    P[0].lineto(P[-1], "orange")
    sleep()
    
    return quickhull_rec (P, 0, len(P) - 1)