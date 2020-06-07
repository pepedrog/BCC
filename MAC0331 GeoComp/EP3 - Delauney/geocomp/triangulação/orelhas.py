#!/usr/bin/env python
"""
Algoritmo de Remoção de Orelhas para Triangulação de Polígonos
Pedro Gigeck Freire - nUSP 10737136
"""

from geocomp.common.segment import Segment
from geocomp.common.prim import left, left_on
from geocomp.common.control import sleep

def intersectaBorda (u, w, P):
    """ Função que recebe dois vértices u e w do polígono P e retorna se o 
        segmento uw intersecta alguma aresta de P
        (equivalente a função QuaseDiagonal dos slides)
    """
    borda = P.edges()
    uw = Segment (u, w)
    for aresta in borda:
        aresta.plot ('cyan')
        sleep()
        if (u not in aresta.endpoints()) and (w not in aresta.endpoints()):
            if (uw.intersects (aresta)):
                aresta.hide()
                aresta.plot('yellow')
                sleep()
                aresta.hide()
                return True
        aresta.hide()
        
    return False

def dentroDoPoligono (u, w, P):
    """ Função que recebe dois vértices u e w do polígono P e retorna se a 
        candidata a diagonal uw está pra dentro do polígono
        (equivalente a função NoCone dos slides)
    """
    prevU = u.prev
    nextU = u.next
    if (left_on (prevU, u, nextU)):
        resposta = (left (u, w, prevU) and left (w, u, nextU))
    else:
        resposta = not (left_on (u, w, nextU) and left_on (w, u, prevU))
    
    if not resposta:
        uw = Segment (u, w)
        uw.plot ("yellow")
        sleep()
        uw.hide()

    return resposta

def isDiagonal (u, w, P):
    """ Função que recebe dois vértices u e w do polígono P e retorna se uw é 
        uma diagonal de P
    """
    # colore a candidata a diagonal
    uw = Segment (u, w)
    uw.plot ('blue')
    sleep()

    # Como o dentroDoPoligono é O(1) é muito prudente fazer esse teste primeiro
    result = dentroDoPoligono (u, w, P) and (not intersectaBorda (u, w, P))
    uw.hide()
    return result

def isOrelha (v, P):
    " Função que recebe um vértice v do polígono P e retorna se v é uma ponta de orelha "
    # despinta de verde e pinta de azul
    if hasattr (v, 'hi'):
        v.unhilight()
    v.hilight('blue')

    resposta = isDiagonal (v.prev, v.next, P)
    v.unhilight()
    
    if resposta:
        v.hilight() #pinta de verde
    sleep()
    return resposta


def Orelhas (p):
    """ Algoritmo que usa a estratégia de encontrar e remover orelhas para triangular o 
        Polígono p[0]
    """
    # Essa é a forma que eu recebo o polígono do front-end :/
    P = p[0]
    n = len(P.vertices())
    
    # Dicionario que relaciona os vértices a um booleano que indica se é orelha
    # Aproveitando que os pontos são 'hashables'
    orelha = dict()
    
    #PreProcessamento dos vértices
    v = P.pts
    orelha[v] = isOrelha (v, P)
    v = v.next
    while v != P.pts:
        orelha[v] = isOrelha (v, P)
        v = v.next
    
    while n > 3:
        # Procura uma orelha
        while not orelha[v]:
            v = v.next
        
        # Sinaliza qual orelha eu escolhi
        v.unhilight()
        v.hilight('red')
        # Desenha a diagonal e desmarca a orelha
        v.prev.lineto (v.next, 'green')
        orelha[v] = False
        sleep()
        
        # Tira v do polígono
        u = v.prev
        w = v.next
        w.prev = u
        u.next = w
        # Essa parte é pra lista sempre ficar circular
        # (P.pts podia ficar inacessivel dai o algoritmo entrava em loop)
        if v == P.pts:
            P.pts = P.pts.next
        
        # Confere se não criei nenhuma orelha
        orelha[u] = isOrelha (u, P)
        orelha[w] = isOrelha (w, P)
        
        v.unhilight()
        n -= 1