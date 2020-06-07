#!/usr/bin/env python
"""Contem as mesmas funcoes do modulo geocomp.common.prim, mas desenhando na tela"""

from . import control
from . import prim
from geocomp import config


def triang (a, b, c, color=config.COLOR_PRIM):
	"desenha  (e apaga) os lados do triangulo abc"
	a.lineto (c, color)
	b.lineto (a, color)
	c.lineto (b, color)
	control.thaw_update ()
	control.update ()
	control.freeze_update ()

	control.sleep ()

	a.remove_lineto (c)
	b.remove_lineto (a)
	c.remove_lineto (b)

def dist2 (a, b, color=config.COLOR_PRIM): 
	"retorna o quadrado da distancia entre a e b"
	ida = a.hilight (color)
	idb = b.hilight (color)
	a.lineto (b, color)
	control.thaw_update ()
	control.update ()
	control.freeze_update ()

	control.sleep ()

	a.remove_lineto (b)
	a.unhilight (ida)
	b.unhilight (idb)

	return prim.dist2(a, b)

def area2 (a, b, c):
	"retorna duas vezes a area do triangulo abc"
	ret = prim.area2 (a, b, c)
	triang (a, b, c)
	return ret

def left (a, b, c):
	"retorna verdadeiro se c esta a esquerda do segmento ab"
	ret = prim.left (a, b, c)
	triang (a, b, c)
	return ret

def right (a, b, c):
	"retorna verdadeiro se c esta a direita do segmento ab"
	ret = prim.right (a, b, c)
	triang (a, b, c)
	return ret

def left_on (a, b, c):
	"retorna verdadeiro se c esta a esquerda ou sobre o segmento ab"
	return not right (a, b, c)

def right_on (a, b, c):
	"retorna verdadeiro se c esta a direita ou sobre o segmento ab"
	return not left (a, b, c)

def collinear (a, b, c):
	"retorna verdadeiro se a, b, c sao colineares"
	ret = prim.collinear (a, b, c)
	triang (a, b, c)
	return ret

#### Beatriz & Igor ####


def float_left (a, b, c):
    "Verdadeiro se c está à esquerda do segmento orientado ab utilizando comparacao de float"
    ret = prim.float_left(a, b, c)
    triang (a, b, c)
    return ret

def float_left_on (a, b, c):
    "Verdadeiro se c está à esquerda ou sobre o segmento orientado ab utilizando comparacao de float"
    ret = prim.float_left_on(a, b, c)
    triang (a, b, c)
    return ret


######################

