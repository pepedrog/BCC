#!/usr/bin/env python
"""
Algoritmo de Remoção de Orelhas para Triangulação de Polígonos
Pedro Gigeck Freire - nUSP 10737136
"""

from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common.polygon import Polygon
from geocomp.common.abbb import Abbb
from geocomp.common.dcel import Dcel
from geocomp.common.prim import left, right_on, left_on
from geocomp.common import control
from .monotono import Monotono

# todo: fazer a dcel
# Debugar a inserção na abbb

class Trapezio:
    # Recebe o vértice de superte v e as duas arestas da esquerda e direita
    def __init__ (self, sup, e = None, d = None):
        self.sup = sup
        if e != None and d != None:
            if e.init.y < e.to.y:
                e.init, e.to = e.to, e.init
            if d.init.y < d.to.y:
                d.init, d.to = d.to, d.init
            self.a_esq = e
            self.a_dir = d
    
    def __eq__ (self, other):
        return (other != None and self.sup != other.sup and
                left_on (self.a_esq.init, self.a_esq.to, other.sup) and
                right_on (self.a_dir.init, self.a_dir.to, other.sup))
    
    def __gt__ (self, other):
        return left (self.a_esq.init, self.a_dir.to, other.sup)
    
    def desenha (self):
        cima = self.sup.y
        baixo = max (self.a_esq.to.y, self.a_dir.to.y)
        
        # Acha os dois pontos da esquerda
        x1, y1 = self.a_esq.init.x, self.a_esq.init.y
        x2, y2 = self.a_esq.to.x, self.a_esq.to.y
        cima_esq = Point ((x2*y1 - x1*y2 + cima*(x1 - x2))/(y1 - y2), cima)
        baixo_esq = Point ((x2*y1 - x1*y2 + baixo*(x1 - x2))/(y1 - y2), baixo)

        # Acha os dois pontos da direita
        x1, y1 = self.a_dir.init.x, self.a_dir.init.y
        x2, y2 = self.a_dir.to.x, self.a_dir.to.y
        cima_dir = Point ((x2*y1 - x1*y2 + cima*(x1 - x2))/(y1 - y2), cima)
        baixo_dir = Point ((x2*y1 - x1*y2 + baixo*(x1 - x2))/(y1 - y2), baixo)
        
        self.aresta_cima = (Segment (cima_esq, cima_dir)).plot('green')
        self.aresta_baixo = (Segment (baixo_esq, baixo_dir)).plot('green')
        self.aresta_esq = (Segment (baixo_esq, cima_esq)).plot('green')
        self.aresta_dir = (Segment (baixo_dir, cima_dir)).plot('green')
        
    def apaga (self):
        control.plot_delete (self.aresta_cima)
        control.plot_delete (self.aresta_baixo)
        control.plot_delete (self.aresta_esq)
        control.plot_delete (self.aresta_dir)
        
    def __str__ (self):
        return str(self.sup) + " " + str(self.a_esq) + " " + str(self.a_dir)
        
def ponta_pra_baixo (p):
    return p.next.y > p.y and p.prev.y > p.y

def trata_caso_meio (p, viz_baixo, L, dcel, diags):
    # Remove da linha o trapésio que tem o p
    t = Trapezio (p)
    removido = (L.busca (t)).elemento
    removido.apaga()
    L.deleta (t)
    
    if ponta_pra_baixo (removido.sup):
        d = Segment (removido.sup, p)
        d.plot('blue')
        dcel.add_edge (d.init, d.to)
        diags.append(d)
        control.sleep()
        
    # Insere um novo trapésio com o p
    # Se o removido estava a direita
    if (p == removido.a_dir.to):
        t.a_dir = Segment (p, viz_baixo)
        t.a_esq = removido.a_esq        
    # Se estava a esquerda
    else:
        t.a_esq = Segment (p, viz_baixo)
        t.a_dir = removido.a_dir
    t.desenha()
    L.insere (t)
    control.sleep()
    
    
def trata_ponta_pra_cima (p, L, dcel, diags):
    viz_esq = p.next
    viz_dir = p.prev
    if left (p, viz_dir, viz_esq):
        viz_esq, viz_dir = viz_dir, viz_esq
    
    t = Trapezio (p)
    removido = (L.busca (t)).elemento
    
    if removido == None:
        t.a_esq = Segment (p, viz_esq)
        t.a_dir = Segment (p, viz_dir)
        t.desenha()
        L.insere (t)
    
    else:
        L.deleta (t)
        removido.apaga()
        d = Segment (p, removido.sup)
        d.plot('blue')
        dcel.add_edge (d.init, d.to)
        diags.append(d)
        control.sleep()
        
        
        t1 = Trapezio (p, removido.a_esq, Segment (p, viz_esq))
        t2 = Trapezio (p, Segment (p, viz_dir), removido.a_dir)
        t1.desenha()
        t2.desenha()
        L.insere (t1)
        L.insere (t2)
        
    control.sleep()
    
def trata_ponta_pra_baixo (p, L, dcel, diags):
    t = Trapezio (p)
    removido1 = (L.busca (t)).elemento
    removido1.apaga()
    L.deleta (t)
    
    if ponta_pra_baixo (removido1.sup):
        d = Segment (removido1.sup, p)
        d.plot('blue')
        control.sleep()
        dcel.add_edge (d.init, d.to)
        diags.append(d)
    
    # Se tem outro polígono
    removido2 = (L.busca (t)).elemento
    if removido2 != None:
        L.deleta (t)
        removido2.apaga()
        
        if ponta_pra_baixo (removido2.sup):
            d = Segment (removido2.sup, p)
            d.plot('blue')
            control.sleep()
            dcel.add_edge (d.init, d.to)
            diags.append(d)
            
        if removido2.a_esq.to == p:
            t = Trapezio (p, removido1.a_esq, removido2.a_dir)
        else:
            t = Trapezio (p, removido2.a_esq, removido1.a_dir)
        L.insere (t)
        t.desenha()
        control.sleep()

def monotonos (d, P, diags):
    """ Função que recebe um polígono P e particiona P em vários polígonos monótonos
        Através da inserção de diagonais
        Coloca as diagonais na DCEL d
    """
    # Ordena os vértices pela Y-coordenada
    v = P.vertices()
    v = sorted(v, key = lambda x:(-x.y))
    
    L = Abbb()
    
    # os vértices são os pontos eventos da linha de varredura
    for p in v:
        p.hilight()
        h = control.plot_horiz_line (p.y)
        control.sleep()
        
        viz_cima = p.next
        viz_baixo = p.prev
        if viz_cima.y < viz_baixo.y:
            viz_cima, viz_baixo = viz_baixo, viz_cima
        
        if viz_cima.y > p.y and p.y > viz_baixo.y:
            trata_caso_meio (p, viz_baixo, L, d, diags)
        elif viz_cima.y < p.y:
            trata_ponta_pra_cima (p, L, d, diags)
        else:
            trata_ponta_pra_baixo (p, L, d, diags) 
        
        control.plot_delete (h)
        p.unhilight()
        
def triangula (P, d):
    """ Função que recebe um polígono monótono P e triangula P, adicionando diagonais
        Concatena as diagonais adicionadas em d
    """
    # Quem faz o trabalho na verdade é a função implementada para o algoritmo
    # de triangulação de polígonos monótonos
    for diag in Monotono ([P]):
        d.append (diag)

def Lee_Preparata (p):
    
    P = p[0]
    diags = []
    d = Dcel ()
    d.initPolygon (P)
    
    # Atualiza a DCEL colocando as diagonais parar a partição em monótonos
    monotonos (d, P, diags)
    n_face_externa = len(P.vertices())
    divisoras = len(diags)
    # Para cada face, constrói um polígono e triangula ele

    if len (d.f) == 2:
        return Monotono([P])

    for e in d.f:
        vertices = [e.init]
        while e.to != vertices[0]:
            vertices.append (e.to)
            e = e.prox
        if len(vertices) != n_face_externa:
            new_p = Polygon (vertices)
            new_p.plot("orange")
            control.sleep()
            # Triangula o new_p e adiciona as novas diagonais no diags
            diags.extend (Monotono ([new_p]))
            new_p.hide()
    
    # despinta as arestas
    for i in range(divisoras):
        diags[i].hide()
        diags[i].plot("green")
        
        
    