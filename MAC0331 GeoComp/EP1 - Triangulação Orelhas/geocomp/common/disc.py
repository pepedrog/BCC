#!/usr/bin/env python

from . import control
from geocomp import config
from geocomp.common.segment import Segment
from geocomp.common.point import Point

class Disc:
	"Um Disco representado por suas coordenadas cartesianas"

	def __init__ (self, x, y, r):
		"Para criar um ponto, passe suas coordenadas."
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
		"Apaga o 'destaque' do ponto"
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
