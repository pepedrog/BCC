#!/usr/bin/env python

from . import control
from geocomp import config
from .vector import Vector
from .prim import dist2

class Point:
    "Um ponto representado por suas coordenadas cartesianas"

    def __init__ (self, *args):
        "Para criar um ponto, passe suas coordenadas."
        if len(args) == 0:
            raise ValueError("Point must have at least one coordinate")
        self.__coord = list(args)
        self.polygon_id = -1
        self.lineto_id = {}

    def __repr__ (self):
        "Retorna uma string da forma '( x1 x2 x3 ... xn )'"
        res = "("
        for i in self.__coord:
            res += " " + repr(i) + ","
        return res[:-1] + " )"

    def __add__(self, other):
        if not isinstance(other, Point) and not isinstance(other, Vector):
            raise ValueError('Cannot add point with non point or vector')
        if other.dimension != self.dimension:
            raise ValueError("Cannot add {0}-d point with {1}-d point" \
                             .format(self.dimension, other.dimension))
        return Point(*[self[i] + other[i] for i in range(self.dimension)])

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return 31 * hash(self.x) + hash(self.y)


    @property
    def dimension(self):
        return len(self.__coord)
    
    @property
    def x(self):
        return self.__coord[0]

    @x.setter
    def x(self, x):
        self.__coord[0] = x

    @property
    def y(self):
        if len(self.__coord) < 2:
            raise ValueError("Point has dimension 1")
        return self.__coord[1]

    @y.setter
    def y(self, y):
        if len(self.__coord) < 2:
            raise ValueError("Point has dimension 1")
        self.__coord[1] = y

    @property
    def z(self):
        if len(self.__coord) < 3:
            raise ValueError("Point does not have dimension 3")
        return self.__coord[2]

    @z.setter
    def z(self, z):
        if len(self.__coord) < 3:
            raise ValueError("Point does not have dimension 3")
        self.__coord[2] = z

    def __getitem__(self, i):
        if i < 0:
            raise ValueError("Negative dimension value")
        if i >= len(self.__coord):
            return 0
        return self.__coord[i]

    def __setitem__(self, key, value):
        if key < 0 or key >= len(self.__coord):
            raise ValueError("Illegal dimension value")
        self.__coord[key] = value

    def plot (self, color=config.COLOR_POINT, radius=config.RADIUS):
        "Desenha o ponto na cor especificada"
        self.plot_id = control.plot_disc (
            self.x,
            self.y,
            color,
            radius
        )
        return self.plot_id

    def unplot(self, id = None):
        if id == None: id = self.plot_id
        control.plot_delete(id)


    def hilight (self, color=config.COLOR_HI_POINT):
        "Desenha o ponto com 'destaque' (raio maior e cor diferente)"
        self.hi = control.plot_disc (self.x, self.y, color,
                        config.RADIUS_HILIGHT)
        return self.hi

    def unhilight (self, id = None):
        "Apaga o 'destaque' do ponto"
        if id == None: id = self.hi
        control.plot_delete (id)

    def lineto (self, p, color=config.COLOR_LINE):
        "Desenha uma linha ate um ponto p na cor especificada"
        self.lineto_id[p] = control.plot_segment (self.x, self.y, p.x, p.y, color)
        return self.lineto_id[p]

    def remove_lineto (self, p, id = None):
        "Apaga a linha ate o ponto p"
        if id == None: id = self.lineto_id[p]
        control.plot_delete (id)

    def distance_to(self, other):
        return dist2(self, other) ** 0.5

    def is_inside(self, segment):
        ''' returns if point is inside the segment. '''
        return segment.has_inside(self)

    def approx_equals(self, other, precision=1e-7):
        for i in range(len(self.__coord)):
            if abs(self[i] - other[i]) >= precision:
                return False
        return True

    

    """
    Ordem dada por y, desempatando por x 
    PS: Usado no projeto do Lucas Moretto de Visibility Graph.
    """
    def __lt__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        if self.x < other.x:
            return True
        return False

    def __le__(self, other):
        if self is other:
            return True
        if type(self) != type(other):
            return False
        if self.y < other.y:
            return True
        if self.y > other.y:
            return False
        if self.x < other.x:
            return True
        if self.x > other.x:
            return False
        return True


#### Bruna & Renan ########

class Edge:

	def __init__(self, v1, v2):
		"Para criar uma aresta, passe suas coordenadas."
		self.point = v1
		self.twin = None
		self.prev = None
		self.next = None

	def __repr__ (self):
		return '( ' + repr(self.point) + ' )'
##########################
    
