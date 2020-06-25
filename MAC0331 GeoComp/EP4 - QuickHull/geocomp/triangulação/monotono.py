#!/usr/bin/env python
"""
Algoritmo de Remoção de Orelhas para Triangulação de Polígonos
Pedro Gigeck Freire - nUSP 10737136
"""

from geocomp.common.segment import Segment
from geocomp.common.prim import right
from geocomp.common.control import sleep


def adj (v1, v2):
    " Função que rev=cebe dois vértices de um polígono e retorna se eles são adjacentes " 
    return (v2 == v1.next or v2 == v1.prev)
 
def ordenaY (P):
    """ Função que recebe um polígono monótono P e retorna uma lista com os vértices
        ordenados pela coordenada Y
    """    
    # acha os extremos do polígono
    cima = P.pts
    p = P.pts.next
    while p != P.pts:
        if p.y > cima.y:
            cima = p
        p = p.next
    
    # vai descendo pelos dois lados, intercalando as duas bordas
    ordenados = []
    p_esq = cima
    p_dir = cima.prev
    while p_esq != p_dir:
        if p_esq.y > p_dir.y:
            ordenados.append (p_esq)
            p_esq = p_esq.next
        else:
            ordenados.append (p_dir)
            p_dir = p_dir.prev
    ordenados.append (p_esq)
    return ordenados
    
def Monotono (p):
    
    # Essa é a forma que eu recebo o polígono do front-end :/
    P = p[0]
    # lista com as diagonais, nosso return
    resp = []

    v = ordenaY (P)
    n = len (v)
    
    s = [v[0], v[1]] # pilha
    v[0].hilight ('blue')
    v[1].hilight ('blue')
    t = 1 # index do fim da pilha
    
    for i in range (2, n):
        v[i].hilight ('green')
        sleep()
        vizinho_ultimo = adj (v[i], s[t])
        vizinho_primeiro = adj (v[i], s[0])
        
        if vizinho_ultimo and not vizinho_primeiro:
            while t > 0:
                a = s[t - 1]
                b = s[t]
                if a.x > b.x:
                    a, b = b, a
                if right (a, b, v[i]):
                    s[t].unhilight()
                    s.pop()
                    t -= 1
                    # acrescenta a nova diagonal
                    d = Segment (s[t], v[i])
                    d.plot ('green')
                    sleep()
                    resp.append (d)
                else: break
            t += 1
            s.append (v[i])
            v[i].unhilight()
            v[i].hilight('blue')
                
        elif vizinho_primeiro and not vizinho_ultimo:
            aux = s[t]
            while t > 0:
                # acrescenta a nova diagonal
                d = Segment (s[t], v[i])
                d.plot ('green')
                sleep()
                resp.append (d)
                
                s.pop()
                t -= 1
                s[t].unhilight()
            s = []
            s.append (aux)
            s.append (v[i])
            v[i].unhilight()
            v[i].hilight ('blue')
            t = 1
                
        else:
            while t > 1:
                s[t].unhilight()
                t -= 1
                # acrescenta a nova diagonal
                d = Segment (s[t], v[i])
                d.plot ('green')
                sleep()
                resp.append (d)
            s[0].unhilight()
            s[1].unhilight()
            v[i].unhilight()
    return resp