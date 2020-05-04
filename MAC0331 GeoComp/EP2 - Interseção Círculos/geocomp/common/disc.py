#!/usr/bin/env python

from . import control
from geocomp import config
from geocomp.common.segment import Segment
from geocomp.common.point import Point
from . import prim

class Disc:
    "Um Disco representado por suas coordenadas cartesianas"

    def __init__ (self, x, y, r):
        "Para criar um disco, passe suas coordenadas."
        self.center = Point(x, y)
        self.r = r
        self.seg = Segment(Point(x-r, y), Point(x+r,y))
        self.lineto_id = {}

    def __repr__ (self):
        "Retorna uma string da forma '( x, y, r )'"
        return '( ' + repr(self.center.x) + ', ' + repr(self.center.y) + ', ' + repr(self.r) + ' )'

    def plot (self, color = config.COLOR_DISC):
        "Desenha o disco na cor especificada"
        self.plot_id = control.plot_disc_grande (self.center.x, self.center.y, color,
                            self.r)
        self.center.plot()
        return self.plot_id

        ################### VICTOR MUDOU  (Edu- talvez n precise disso) #######################

    def unplot(self, id = None):
        if id == None: id = self.plot_id
        control.plot_delete(id)



        ################## FIM ############################

    def hilight (self, color=config.COLOR_HI_POINT):
        "Desenha o disco com 'destaque' (com cor diferente)"
        self.hi = control.plot_disc (self.center.x, self.center.y, color,
                        self.r)
        return self.hi
    
    def unhilight (self, id = None):
        "Apaga o 'destaque' do disco"
        if id == None: id = self.hi
        control.plot_delete (id)
    
    def lineto (self, p, color=config.COLOR_LINE):
        "Desenha uma linha do centro até o ponto especificado"
        self.lineto_id[p] = control.plot_line (self.center.x, self.center.y, p.x, p.y, color)
        return self.lineto_id[p]
    
    def remove_lineto (self, p, id = None):
        "Remove a linha ate o ponto p"
        if id == None: id = self.lineto_id[p]
        control.plot_delete (id)

    def extremes(self):
        
        offsets = [self.r, - self.r]

        return [ self.center + Point(0, off) for off in offsets] + [ self.center + Point(off, 0) for off in offsets]
    
    ################ PEDRO GF MUDOU ##########################################
    
    def hilight_circ (self, color = "yellow", width = 2):
        "Desenha a circunferência (contorno) com destaque"
        self.circ_id = control.plot_circle (self.center.x, self.center.y, color, self.r, width = width)
        return self.circ_id
    
    def unhilight_circ (self, id = None):
        "Apaga o destaque da circunferência (contorno)"
        if id == None: id = self.circ_id
        control.plot_delete (id)
    
    def hilight_semi_circle (self, up, color="red", width = 2):
        "Desenha o meio circulo, up indica se é a metade de cima ou de baixo"
        if up:
            self.id_semi_up = control.plot_semi_circle (self.center.x, self.center.y, self.r, up, color, width = width)
            return self.id_semi_up
        self.id_semi_down = control.plot_semi_circle (self.center.x, self.center.y, self.r, up, color, width = width)
        return self.id_semi_down
    
    def unhilight_semi_circle (self, up):
        "Apaga o semi_circulo"
        if up:
            return control.plot_delete (self.id_semi_up)
        return control.plot_delete (self.id_semi_down)
    
    def intersects_circ (self, other):
        "Confere se a circunferência do disco intersecta com a circunferência do other"
        d = (prim.dist2 (self.center, other.center))**0.5
        sum_r = self.r + other.r
        
        # Deixa o menor no self
        if self.r > other.r:
            self, other = other, self
            
        # Confere se o menor não está dentro do maior
        if d + self.r < other.r:
            return False
        
        # Confere se os discos se intersectam
        if d <= sum_r and d :
            return True
        else:
            return False
    
    def intersection (self, other):
        "Retorna uma lista com o(s) ponto(s) de interseção entre os dois círculos"
        if not self.intersects_circ (other):
            return []
        
        # Um pouco de geometria: Montando a esquação do circulo
        # Temos: self: (x - x1)^2 + (y - y1)^2 = r1^2
        #       other: (x - x2)^2 + (y - y2)^2 = r2^2
        x1, y1 = self.center.x, self.center.y
        x2, y2 = other.center.x, other.center.y
        r1, r2 = self.r, other.r
        
        # Depois de subtrair as duas equações, teremos uma reta
        # 2x*(x2 - x1) + 2y*(y2 - y1) + x1^2 - x2^2 + y1^2 - y2^2 = r1^2 - r2^2
        
        # Isolando o x para a resposta, temos essa grande conta:
        # x = [ r1^2 - r2^2 + x2^2 - x1^2 + y2^2 - x1^2 + 2y*(y2 - y1) ] / 2*(x2 - x1)
        
        # se x1 = x2, temos um caso mais simples, basta encontrar y
        if x1 == x2:
            if y1 == y2:
                # supondo que não há circulos iguais
                return []
            res_y1 = (r1**2 - r2**2 + y2**2 - y1**2) / (2*(y2 - y1))
            res_y2 = res_y1
            res_x1 = (r1**2 - (res_y1 - y1)**2 )**(0.5) + x1
            res_x2 = -(r1**2 - (res_y1 - y1)**2 )**(0.5) + x1
        
        # Se não, temos que colocar o x em alguma das equações dos circulos e criar uma equação de 2º grau
        # Depois de (( muitas )) continhas ... 
        # conclui que os valores de a, b e c para nossa equação ay^2 + by + c = 0 são
        else:
            const = r1**2 - r2**2 + y2**2 - y1**2 + x2**2 + x1**2 - 2*x1*x2 
            
            a = (y1 - y2)**2 / (x1 - x2)**2 + 1
            b = (y1 - y2)*const / (x1 - x2)**2 - 2*y1
            c = const**2 / (4*(x1 - x2)**2) + y1**2 - r1**2
            
            # Agora a gente aplica um super bhaskara
            delta = b**2 - 4*a*c
            res_y1 = (-b + delta**(0.5)) / (2*a)
            res_y2 = (-b - delta**(0.5)) / (2*a)
            
            # Aplica os valores na reta para descobir os x
            res_x1 = ( r1**2 - r2**2 + y2**2 - y1**2 + x2**2 - x1**2 + 2*res_y1*(y1 - y2) ) / (2*(x2 - x1))
            res_x2 = ( r1**2 - r2**2 + y2**2 - y1**2 + x2**2 - x1**2 + 2*res_y2*(y1 - y2) ) / (2*(x2 - x1))
        
        p1 = Point (res_x1, res_y1)
        p2 = Point (res_x2, res_y2)
        if p1.approx_equals (p2):
            return [p1]
        return [p1, p2]
        
    ################### FIM PEDRO ######################################