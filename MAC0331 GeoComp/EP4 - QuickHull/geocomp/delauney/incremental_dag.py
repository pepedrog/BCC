# -*- coding: utf-8 -*-
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.common.prim import left, left_on
from geocomp.common.dcel import Dcel
from geocomp.common.control import sleep
from random import shuffle

# A única diferença desse arquivo pro incremental.py é o valor dessa flag
desenha_busca = True

color_triang = "orange"
color_novo = "firebrick"
color_legalizaveis = "green"
color_ilegal = "red"

# Os tres pontos no infinito
global infs

class Node_Triang:
    " Classe que será o nó do DAG, guarda os triângulos que fazem parte da triangulação "
    def __init__ (self, p1, p2, p3, a):
        if left (p1, p2, p3):
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1
        self.p3 = p3
        self.a = a # Alguma aresta da DCEL que faz parte desse triangulo
        self.filhos = [] # Node_Triangs que são filhos do self no DAG
        # arestas
        self.a1 = Segment (self.p1, self.p2)
        self.a2 = Segment (self.p2, self.p3)
        self.a3 = Segment (self.p3, self.p1)
    
    def draw (self):
        self.a1.plot("gray")
        self.a2.plot("gray")
        self.a3.plot("gray")
        sleep()
    
    def hide (self):
        self.a1.hide()
        self.a2.hide()
        self.a3.hide()
        
    def busca (self, ponto):
        " Retorna o nó folha em que o ponto está "
        if desenha_busca: self.draw()
        for f in self.filhos:
            if (left_on (f.p1, f.p2, ponto) and 
                left_on (f.p2, f.p3, ponto) and
                left_on (f.p3, f.p1, ponto)):
                if desenha_busca: self.hide()
                return f.busca (ponto)
        if desenha_busca: self.hide()
        return self 

def pontos_infinitos (p):
    " Devolve três pontos fictícios tais que o triangulo formado por eles "
    " contém todos os pontos de p "
    
    # Vou montar um quadradão que contém todos os pontos
    cima = baixo = direito = esquerdo = p[0]
    for i in range(1, len(p)):
        if p[i].y > cima.y: cima = p[i]
        if p[i].y < baixo.y: baixo = p[i]
        if p[i].x < esquerdo.x: esquerdo = p[i]
        if p[i].x > direito.x: direito = p[i]
        
    # Agora monto um triângulão que contém esse quadrado
    p1 = Point (esquerdo.x - 10*(direito.x - esquerdo.x), baixo.y - 10*(cima.y - baixo.y))
    p2 = Point (esquerdo.x + (direito.x - esquerdo.x)/2, cima.y + 10*(cima.y - baixo.y))
    p3 = Point (esquerdo.x + 10*(direito.x - esquerdo.x), baixo.y - 10*(cima.y - baixo.y))
    return p1, p2, p3

def add_triangs_dcel (d, p, triang):
    " Adiciona o P na dcel d e uma aresta de p pra cada ponta do triang "
    d.add_vertex (p)
    e1 = d.add_edge (p, triang.p1, triang.a.f)
    e2 = d.add_edge (p, triang.p2, triang.a.f)
    e3 = d.add_edge (p, triang.p3, e2.f)
    e1.draw(color_novo)
    e2.draw(color_novo)
    e3.draw(color_novo)
    sleep()
    return e1, e2, e3

def ilegal (e):
    " Devolve se a aresta dada pela meia aresta 'e' é ilegal "
    # As arestas do triangulão infinito não podem ser ilegais
    global infs
    if e.init in infs and e.to in infs:
        return False
    
    e.draw(color_legalizaveis)
    sleep()
    # O quadrilatero precisa ser convexo
    if left (e.twin.prox.to, e.to, e.prox.to) == left (e.twin.prox.to, e.init, e.prox.to):
        return False

    def angulo (p1, p2, p3):
        " Devolve algo proporcional ao angulo em p2 de p1-p2-p3 "
        # Na verdade, devolve o -2*cosseno do angulo com a lei do cosseno
        a2 = (p3.x - p1.x)**2 + (p3.y - p1.y)**2
        b2 = (p3.x - p2.x)**2 + (p3.y - p2.y)**2
        c2 = (p1.x - p2.x)**2 + (p1.y - p2.y)**2
        ang = ((b2 + c2 - a2)/(2*((b2*c2)**0.5)))
        return -ang
        # Como cosseno é descrescente para angulos menores que pi,
        # Então posso comparar dois angulos a e b pelos seus cossenos
        # a > b <=> cos(a) < cos(b)
    
    # Acha o menor angulo do triangulo com a aresta e
    min_ang1 = min ([angulo (e.prev.init, e.init, e.to),
                     angulo (e.init, e.to, e.prev.init),
                     angulo (e.to, e.prev.init, e.init)])
    # Acha o menor angulo do triangulo com a aresta e.twin
    min_ang2 = min ([angulo (e.twin.prev.init, e.init, e.to),
                     angulo (e.init, e.to, e.twin.prev.init),
                     angulo (e.init, e.twin.prev.init, e.to)])
    min_ang_legal = min(min_ang1, min_ang2)

    # Acha o menor angulo dos triangulos com a outra diagonal
    min_ang1 = min ([angulo (e.prev.init, e.init, e.twin.prev.init),
                     angulo (e.init, e.prev.init, e.twin.prev.init),
                     angulo (e.prev.init, e.twin.prev.init, e.init)])
    min_ang2 = min ([angulo (e.prev.init, e.to, e.twin.prev.init),
                     angulo (e.to, e.prev.init, e.twin.prev.init),
                     angulo (e.prev.init, e.twin.prev.init, e.to)])
    min_ang_ilegal = min(min_ang1, min_ang2)
    return min_ang_legal < min_ang_ilegal

def trata_degenerado_aresta (d, p, triang):
    if triang.a1.has_inside(p):
        d.remove_edge (triang.p1, triang.p2)
        
        return []
        
    if triang.a2.has_inside(p):
        d.remove_edge (triang.p2, triang.p3)
        return []
    
    if triang.a3.has_inside(p):
        d.remove_edge (triang.p3, triang.p1)
        return []
        
    return []

def Incremental (pontos):
    " Função principal: Recebe uma coleção de pontos e retorna uma DCEL da triangulão "
    " de Delauney desses pontos, desenhando os passos do algoritmo na tela "
    d = Dcel()
    if len(pontos) < 3: return []
    
    global infs
    global desenha_busca
    shuffle (pontos)
    
    inf1, inf2, inf3 = pontos_infinitos (pontos)
    infs = [inf1, inf2, inf3]
    
    # Cria o triangulo auxiliar grandão que contém toda a coleção
    raiz = Node_Triang (inf1, inf2, inf3, None)
    d.add_vertex (inf1)
    d.add_vertex (inf2)
    d.add_vertex (inf3)
    e1 = d.add_edge (inf1, inf2)
    e2 = d.add_edge (inf2, inf3)
    e3 = d.add_edge (inf3, inf1)
    raiz.a = e1.twin
    
    # Toda vez que criarmos uma face vamos ter que associar a folha do dag a essa face
    d.extra_info[e1.f] = raiz

    # Processamento principal
    for p in pontos:
        p.hilight(color_novo)
        triang = raiz.busca (p)
        sleep()
        
        # Caso degenerado
        # 1. Pontos Coincidentes -> Apenas ignoro
        if p == triang.p1 or p == triang.p2 or p== triang.p3:
            p.unhilight()
            continue
        # Caso geral
        else:
            # Adiciona as três arestas na dcel
            e1, e2, e3 = add_triangs_dcel (d, p, triang)
            novas = [e1, e2, e3]
            # Adiciona as novas faces/triangulos no dag e dcel
            novos_triangs = [Node_Triang (triang.p1, triang.p2, p, e1),
                             Node_Triang (triang.p2, triang.p3, p, e2),
                             Node_Triang (triang.p3, triang.p1, p, e3)]
            for t in novos_triangs:
                triang.filhos.append (t)
                d.extra_info[t.a.f] = t
                
            # Legaliza arestas
            legalizaveis = [e1.prox, e2.prox, e3.prox]

        while len (legalizaveis) > 0:
            e = legalizaveis.pop()
            
            if not ilegal (e):
                e.draw(color_triang)  
            else:
                e.draw(color_ilegal)
                sleep()
                # Guarda os triangulos que serão 'removidos' das folhas do dag
                pai1 = d.extra_info[e.f]
                pai2 = d.extra_info[e.twin.f]
                
                # Revome a diagonal ilegal e adiciona a legal
                d.remove_edge (e)
                e_nova = d.add_edge (e.prox.to, e.twin.prox.to, e.prox.f)
                novas.append(e_nova)
                e_nova.draw(color_novo)
                
                # Adiciona os novos triangulos no dag
                t1 = Node_Triang (e.to, e.prox.to, e.twin.prox.to, e_nova)
                t2 = Node_Triang (e.init, e.prox.to, e.twin.prox.to, e_nova.twin)
                pai1.filhos = pai2.filhos = [t1, t2]
                # referencia as novas folhas do dag para suas faces na dcel
                d.extra_info[e_nova.f] = t1
                d.extra_info[e_nova.twin.f] = t2
                # Adiciona as arestas dos novos triangs na fila de legalizáveis
                for l in [e_nova.prox, e_nova.prev, e_nova.twin.prox, e_nova.twin.prev]:
                    if l.init != p and l.to != p:
                        legalizaveis.append(l)
                sleep()
        # Recolore as arestas que estavam com a outra cor
        for e in novas:
            e.draw(color_triang)
        p.unhilight()
    
    # Depois de processar todos os pontos, removo os pontos do infinito
    for i in infs:
        rem = d.v[i].twin.prox
        while rem != d.v[i]:
            d.remove_edge(rem)
            rem = rem.twin.prox
        d.remove_edge(rem)
        d.v.pop(i)
        sleep()
    # Por algum motivo quando eu retorno a DCEL buga a tela :(
    return [d]
        