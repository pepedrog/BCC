#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

"""Primitivas geometricas usadas nos algoritmos

Use o modulo geocomp.common.guiprim para que essas primitivas sejam
desenhadas na tela  medida que elas so usadas. Tambm  possvel
desenh-las de um jeito especfico para um determinado algoritmo.
Veja geocomp.convexhull.quickhull para um exemplo.
"""

######## MORETTO #########
COLIN_TOLERANCE = 10
T  = 10 ** COLIN_TOLERANCE
T2 = 10.0 ** COLIN_TOLERANCE

SMALLEST_NUM = 0.00000001
INFINITY     = 100000

############################

# Numero de vezes que a funcao area2 foi chamada
num_area2 = 0
# Numero de vezes que a funcao dist2 foi chamada
num_dist = 0

def count_area2():
    global num_area2
    num_area2 = num_area2 + 1

def area2 (a, b, c):
    "Retorna duas vezes a area do tringulo determinado por a, b, c"
    global num_area2
    num_area2 = num_area2 + 1
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def area_sign(a, b, c):
    area = area2(a, b, c)
    if area > 0:
        return 1
    if area < 0:
        return -1
    return 0

def left (a, b, c):
    "Verdadeiro se c est  esquerda do segmento orientado ab"
    return area2 (a, b, c) > 0

def left_on (a, b, c):
    "Verdadeiro se c est  esquerda ou sobre o segmento orientado ab"
    return area2 (a, b, c) >= 0

def collinear (a, b, c):
    "Verdadeiro se a, b, c sao colineares"
    return area2 (a, b, c) == 0

def right (a, b, c):
    "Verdadeiro se c est  direita do segmento orientado ab"
    return not (left_on (a, b, c))

def right_on (a, b, c):
    "Verdadeiro se c est  direita ou sobre o segmento orientado ab"
    return not (left (a, b, c))

def dist2 (a, b):
    "Retorna o quadrado da distancia entre os pontos a e b"
    global num_dist
    num_dist = num_dist + 1
    dy = b.y - a.y
    dx = b.x - a.x

    return dy*dy + dx*dx

def get_count ():
    "Retorna o numero total de operacoes primitivas realizadas"
    return num_area2 + num_dist

def reset_count ():
    "Zera os contadores de operacoes primitivas"
    global num_area2, num_dist
    num_area2 = 0
    num_dist = 0

def ccw_angle(u, v):
    if u is None or v is None:
        raise ValueError("Illegal argument of None type")
    dot   = u[0] * v[0] + u[1] * v[1]
    det   = u[0] * v[1] - u[1] * v[0]
    theta = math.atan2(det, dot)

    if theta >= 0:
        return theta
    return 2.0 * math.pi + theta

def cw_angle(u, v):
    if u is None or v is None:
        raise ValueError("Illegal argument of None type")
    dot   = u[0] * v[0] + u[1] * v[1]
    det   = u[0] * v[1] - u[1] * v[0]
    theta = math.atan2(det, dot)

    if theta < 0:
        return 2 * math.pi + theta
    return theta

def cross(u, v):
    if u is None or v is None:
        raise ValueError("Illegal argument of None type")

    if len(u) != len(v):
        raise ValueError("Vectors have different dimensions")

    dim = len(u)
    w = []
    for i in range(dim):
        w.append(0)
        for j in range(dim):
            if j != i:
                for k in range(dim):
                    if k != i:
                        if k > j:
                            w[i] += u[j] * v[k]
                        elif k < j:
                            w[i] -= u[j] * v[k]
    return w


def intersect(a, b, c, d):
    if a is None or \
       b is None or \
       c is None or \
       d is None:
        raise ValueError("Points must not be None")

    if intersect_prop(a, b, c, d):
        return True

    if on_segment(a, b, c) or \
       on_segment(a, b, d) or \
       on_segment(c, d, a) or \
       on_segment(c, d, b):
        return True
    return False


# TODO: Não trata o caso de todos os pontos colineares mas ainda com
# uma interseção própria.
#
# Ex: [(0,0), (2,0)] e [(1,0), (3,0)]
# retornaria que não intersecta propriamente, quando an verdade seus
# interiores se tocam
def intersect_prop(a, b, c, d):
    if a is None or \
       b is None or \
       c is None or \
       d is None:
        raise ValueError("Points must not be None")

    if collinear(a, b, c) or \
       collinear(a, b, d) or \
       collinear(a, c, d) or \
       collinear(b, c, d):
        return False

    return left(a, b, c) ^ left(a, b, d) and \
           left(c, d, a) ^ left(c, d, b)

def on_segment(a, b, c):
    if a is None or \
       b is None or \
       c is None:
        raise ValueError("Points must not be None")

    if not collinear(a, b, c):
        return False

    if a.x != b.x:
        return \
            a.x <= c.x <= b.x or \
            b.x <= c.x <= a.x
    return \
        a.y <= c.y <= b.y or \
        b.y <= c.y <= a.y



def dot(u, v):
    return u.x * v.x + u.y * v.y

def perp(a, b):
    if a is None or b is None:
        raise ValueError("Illegal argument of None type")
    return a.x * b.y - a.y * b.x

#### Beatriz & Igor ######

# epsilon do erro
ERR = 1.0e-5


def cmpFloat(a, b):
	"Comparacao de float com margem de erro com preferencia para a igualdade"
	if (abs(a-b) < ERR):
		return 0
	elif (a + ERR > b):
		return 1
	return -1

def float_left (a, b, c):
	"Verdadeiro se c est  esquerda do segmento orientado ab utilizando comparacao de float"
	if(cmpFloat(area2 (a, b, c), 0) == 1):
		return True
	return False

def float_left_on (a, b, c):
	"Verdadeiro se c est  esquerda ou sobre o segmento orientado ab utilizando comparacao de float"
	if(cmpFloat(area2 (a, b, c), 0) == 0):
		return True
	return False
############


############ Moretto ##############
def intersection_point(a, b, c, d):
    if a is None or \
       b is None or \
       c is None or \
       d is None:
        raise ValueError()
    u = b - a
    v = d - c
    w = a - c
    d = perp(u, v)

    if abs(d) < SMALLEST_NUM:
        if perp(u, w) != 0 or perp(v, w) != 0:
            return None

        du = dot(u, u)
        dv = dot(v, v)
        if du == 0 and dv == 0:
            if a != c:
                return None
            return a

        if du == 0:
            if not on_segment(c, d, a):
                return None
            return a
        if dv == 0:
            if not on_segment(a, b, c):
                return None
            return c

        w2 = b - c
        if v[0] != 0:
            t0 = w[0] / v[0]
            t1 = w2[0] / v[0]
        else:
            t0 = w[1] / v[1]
            t1 = w2[1] / v[1]

        if t0 > t1:
            t = t0
            t0 = t1
            t1 = t

        if t0 > 1 or t1 < 0:
            return None

        if t0 < 0:
            t0 = 0
        if t1 > 1:
            t1 = 1
        if t0 == t1:
            return c + Point(t0 * v[0], t0 * v[1])

        p0 = c + Point(t0 * v[0], t0 * v[1])
        p1 = c + Point(t1 * v[0], t1 * v[1])
        return Segment(p0, p1)

    si = perp(v, w) / d
    if si < 0 or si > 1:
        return None

    ti = perp(u, w) / d
    if ti < 0 or ti > 1:
        return None
    return a + Point(si * u[0], si * u[1])


def intersection_dist2(p1, p2, edge):
    common = intersection_point(p1, p2, edge.p1, edge.p2)
    if common is not None:
        if type(common) is Segment:
            return dist2(p1, common.upper)
        return dist2(p1, common)
    return 0


def segment_in_poly(a, b, poly):
    if a is None or \
       b is None or \
       poly is None:
        raise ValueError("Illegal argument of None type")

    v = poly.vertices()

    if len(v) < 3:
        raise ValueError("Polygon must have at least three vertices")

    if a == b:
        return point_in_polygon(a, poly)

    te = 0.0
    tl = 1.0
    ds = b - a
    v.append(v[0])

    for i in range(len(v) - 1):
        e = v[i + 1] - v[i]
        N = perp(e, a - v[i])
        D = -perp(e, ds)
        if abs(D) < SMALLEST_NUM:
            if N < 0:
                return False
            continue

        t = N / D
        if D < 0:
            if t > te:
                te = t
                if te > tl:
                    return False
        elif t < tl:
            tl = t
            if tl < te:
                return False

    p0 = a + Point(te * ds[0], te * ds[1])
    p1 = a + Point(tl * ds[0], tl * ds[1])
    p_mid = Point((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
    return point_in_polygon(p_mid, poly)


def angle(p0, p1, p2):
    a   = (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2
    b   = (p2[0] - p0[0]) ** 2 + (p2[1] - p0[1]) ** 2
    c   = (p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2
    cos = (a + c - b) / (2 * math.sqrt(a) * math.sqrt(c) + COLIN_TOLERANCE)
    return math.acos(int(cos * T) / T2)

def intersection_dist2(p1, p2, edge):
    common = intersection_point(p1, p2, edge.p1, edge.p2)
    if common is not None:
        if type(common) is Segment:
            return dist2(p1, common.upper)
        return dist2(p1, common)
    return 0

#################################3

