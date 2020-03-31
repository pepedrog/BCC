#!/usr/bin/env python

from . import control
from geocomp import config
from .prim import area2, left


class Segment:
    "Um segmento de reta"
    def __init__ (self, pto_from=None, pto_to=None):
        "Para criar, passe os dois pontos extremos"
        self.init  = pto_from
        self.to = pto_to
        if self.__cmp(self.init, self.to) < 0:
            self.upper = self.init
            self.lower = self.to
        else:
            self.upper = self.to
            self.lower = self.init

    def __repr__ (self):
        "retorna uma string da forma [ ( x0 y0 );( x1 y1 ) ]"
        return '[ ' + repr(self.init) + '; ' + repr(self.to) + ' ]'

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.init == other.init and self.to == other.to:
            return True
        if self.init == other.to and self.to == other.init:
            return True
        return False

    def endpoints(self):
        return self.init, self.to

    def hilight (self, color_line=config.COLOR_HI_SEGMENT,
            color_point=config.COLOR_HI_SEGMENT_POINT):
        "desenha o segmento de reta com destaque na tela"
        self.lid = self.init.lineto (self.to, color_line)
        self.pid0 = self.init.hilight (color_point)
        self.pid1 = self.to.hilight (color_point)
        return self.lid

    def unhilight (self):
        control.plot_delete (self.lid)
        control.plot_delete (self.pid0)
        control.plot_delete (self.pid1)

    def plot (self, cor=config.COLOR_SEGMENT):
        "desenha o segmento de reta na tela"
        self.lid = self.init.lineto (self.to, cor)
        return self.lid

    def hide (self, id=None):
        "apaga o segmento de reta da tela"
        if id is None: id = self.lid
        control.plot_delete (id)

    def has_left(self, point):
        return left(self.init, self.to, point)

    def colinear_with(self, point):
        ''' returns if point is colinear with the segment. '''
        return area2(self.init, self.to, point) == 0

    def has_inside(self, point):
        ''' returns if point is inside the segment. '''
        if not self.colinear_with(point):
            return False
        if self.init.x != self.to.x:
            return self.init.x <= point.x <= self.to.x \
                   or self.to.x <= point.x <= self.init.x
        else:
            return self.init.y <= point.y <= self.to.y \
                   or self.to.y <= point.y <= self.init.y

    def intersects_inside(self, other_segment) -> bool:
        ''' returns whether the other segment intersects this segment
            (not counting border points) '''
        if self.colinear_with(other_segment.init)    \
           or self.colinear_with(other_segment.to)   \
           or other_segment.colinear_with(self.init) \
           or other_segment.colinear_with(self.to):
            return False

        return (left(self.init, self.to, other_segment.init)
                ^ left(self.init, self.to, other_segment.to))            \
               and (left(other_segment.init, other_segment.to, self.init)
                   ^ left(other_segment.init, other_segment.to, self.to))


    def intersects(self, other_segment) -> bool:
        if self.intersects_inside(other_segment):
            return True

        return self.has_inside(other_segment.init)    \
               or self.has_inside(other_segment.to)   \
               or other_segment.has_inside(self.init) \
               or other_segment.has_inside(self.to)

    def adj(self, p):
        if p == self.init:
            return self.to
        return self.init

    def __hash__(self):
        return hash(self.init) ^ hash(self.to)

    def __cmp(self, a, b):
        if(type(a) != Segment or type(b) != Segment):
            return 1
        if a[1] > b[1]:
            return -1
        if b[1] > a[1]:
            return 1
        if a[0] < b[0]:
            return -1
        if b[0] < a[0]:
            return 1
        return 0

    # TODO: Teste de contains testa se ponto é uma das pontas da
    # aresta, mas faz mais sentido ver se o ponto estar dentro da
    # aresta como um todo. Mas estou mantento isso no momento para
    # manter compatibilidade com o projeto de Visibility Graph do
    # Lucas Moretto.
    def __contains__(self, p):
        return p == self.init or p == self.to


    # A baixo seguem setters e getters para atributos para manter
    # compatibilidade com o projeto de Visibility Graph do Lucas
    # Moretto.

    @property
    def p1(self):
        return self.init

    @p1.setter
    def p1(self, p1):
        self.init = p1

    @property
    def p2(self):
        return self.to

    @p1.setter
    def p2(self, p2):
        self.init = p2
