#!/usr/bin/env python
"""Implementacao das operacoes graficas em Tk.

Esse modulo nao deve ser usado diretamente. Para isso,
veja geocomp.common.control"""

from math import fabs

master = None
canvas = None

def init_display (master):
	globals()['canvas'] = master.canvas
	globals()['master'] = master

def get_canvas ():
	return canvas

def update ():
	canvas.update ()

def sleep ():
	if master.step_by_step.get ():
		master.tk.wait_variable (master.step)
	else:
		master.tk.after (master.delay.get (), master.tk.quit)
		master.tk.mainloop ()

def plot_disc (x, y, color, r):
	plot_id = canvas.create_oval (canvas.r2cx(x)-r, canvas.r2cy(y)-r, 
					canvas.r2cx(x)+r, canvas.r2cy(y)+r, fill=color)
	return plot_id

def plot_segment (x0, y0, x1, y1, color, linewidth):
	lineto_id = canvas.create_line (canvas.r2cx(x0), canvas.r2cy(y0), 
					   canvas.r2cx(x1), canvas.r2cy(y1), 
					   fill=color, width=linewidth)
	return lineto_id

def find_intersection_points(x0, y0, x1, y1):
	"""retorna os dois pontos que a reta passando pelos pontos dos argumentos 
	intersecta com as bordas do canvas
	"""

	x0 = float (canvas.r2cx(x0))
	y0 = float (canvas.r2cy(y0))
	x1 = float (canvas.r2cx(x1))
	y1 = float (canvas.r2cy(y1))

	if x0 == x1: 
		return x0, 0, x1, float (canvas['height'])
	if y0 == y1:
		return 0, y0, float (canvas['width']), y1

	dy, dx = (y1 - y0), (x1 - x0)
	
	"pontos candidatos a estarem na resposta"
	x = [0] * 4
	y = [0] * 4

	"intersecao com as quatro retas da borda do canvas:"

	"intersecao com reta vertical: (0, 0) e (0, canvas['height'])"
	x[0] = 0.
	alpha = (x[0] - x0) / dx
	y[0] = alpha * dy + y0

	"intersecao com reta horizontal: (0, canvas['height']) e (canvas['width'], canvas['height'])"
	y[1] = float (canvas['height'])
	alpha = (y[1] - y0) / dy
	x[1] = alpha * dx + x0

	"intersecao com reta vertical: (canvas['width'], canvas['height']) e (canvas['width'], 0)"
	x[2] = float (canvas['width']) 
	alpha = (x[2] - x0) / dx
	y[2] = alpha * dy + y0

	"intersecao com reta horizontal: (canvas['width'], 0) e (0, 0)"
	y[3] = 0.
	alpha = (y[3] - y0) / dy
	x[3] = alpha * dx + x0	

	"pontos na resposta"
	ret_x = []
	ret_y = []

	"Encontra os dois pontos que estão na borda do canvas"

	"borda vertical esquerda"
	if y[0] >= 0 and y[0] <= float (canvas['height']):
		ret_x.append(x[0])
		ret_y.append(y[0])

	"borda horizontal superior"
	if x[1] >= 0 and x[1] <= float (canvas['width']):
		ret_x.append(x[1])
		ret_y.append(y[1])

	"borda vertical direita"
	if y[2] >= 0 and y[2] <= float (canvas['height']):
		ret_x.append(x[2])
		ret_y.append(y[2])

	"borda horizontal inferior"
	if x[3] >= 0 and x[3] <= float (canvas['width']):
		ret_x.append(x[3])
		ret_y.append(y[3])

	return ret_x[0], ret_y[0], ret_x[1], ret_y[1]

def plot_line (x0, y0, x1, y1, color, linewidth):
	x2, y2, x3, y3 = find_intersection_points(x0, y0, x1, y1) 
	lineto_id = canvas.create_line (int (x2), int (y2), int (x3), int (y3), 
					   fill=color, width=linewidth)
	return lineto_id

def inner_product(x0, y0, x1, y1):
	return x0 * x1 + y0 * y1

def plot_ray (x0, y0, x1, y1, color, linewidth):
	"trocando para coordenadas do canvas"
	x2, y2, x3, y3 = find_intersection_points(x0, y0, x1, y1)

	x0 = float (canvas.r2cx(x0))
	y0 = float (canvas.r2cy(y0))
	x1 = float (canvas.r2cx(x1))
	y1 = float (canvas.r2cy(y1))
	
	"""decide qual ponto (que será guardado em (x2, y2)) formará com (x0, y0)
	o segmento que representará a semi-reta"""
	if inner_product((x2 - x0), (y2 - y0), (x1 - x0), (y1 - y0)) < 0: 
		x2, y2 = x3, y3

	lineto_id = canvas.create_line (int (x0), int (y0), 
					   int (x2), int (y2), 
					   fill=color, width=linewidth)	
	return lineto_id						 

def plot_vert_line (x, color, linewidth):
	lineto_id = canvas.create_line (canvas.r2cx(x), 0, 
					   canvas.r2cx(x), int (canvas['height']), 
					   fill=color, width=linewidth)
	return lineto_id

def plot_horiz_line (y, color, linewidth):
	lineto_id = canvas.create_line (0, canvas.r2cy(y), 
					   int (canvas['width']), canvas.r2cy(y), 
					   fill=color, width=linewidth)
	return lineto_id

def plot_parabola(y,px,py,startx,endx,steps,color,linewidth):
	if startx == endx or py == y:
		line_id = canvas.create_line (px,py,px,y,fill=color,width=linewidth)
		return line_id
	if startx > endx:
		startx,endx = endx,startx
	Dx = (endx - startx)/(steps)
	x = startx
	curve = []
	for i in range(steps+1):
		yn = (px*px - 2*px*x + x*x + py*py - y*y)/(2*(py-y))
		curve.append(canvas.r2cx(x))
		curve.append(canvas.r2cy(yn))
		x = x + Dx
	line_id = canvas.create_line (curve,fill=color,width=linewidth)
	return line_id

def plot_delete (id):
	canvas.delete (id)

def config_canvas (minx, maxx, miny, maxy):
	for item in canvas.find_all ():
		canvas.delete (item)


	Dx = maxx - minx
	Dy = maxy - miny

	if canvas.winfo_width () <= 1 and canvas.winfo_height () <= 1:
		width = int (canvas['width'])
		height = int (canvas['height'])
	else:
		width = canvas.winfo_width ()
		height = canvas.winfo_height ()

	ratio = float (width)/ float (height)
	ratio_dxdy = float (Dx)/ float (Dy)

	if ratio != ratio_dxdy:
		if ratio_dxdy < ratio:
			new_dx = Dy * ratio
			minx = minx - fabs (Dx-new_dx)/2
			Dx = new_dx
		else:
			new_dy = Dx / ratio
			miny = miny - fabs (Dy-new_dy)/2
			Dy = new_dy


	def rx (x, x0 = minx, dx = Dx, width=width):
		return int ((x - x0) * width*0.8 / dx + 0.1*width)
		#return int ((x - x0) * int (cv['width'])*0.8 / dx + 0.1*int (cv['width']))

	def ry (y, y0 = miny, dy = Dy, height=height):
		return height - int ((y - y0) * height*0.8 / dy + 0.1*height)
		#return int (cv['height']) - int ((y - y0) * int (cv['height'])*0.8 / dy + 0.1*int (cv['height']))

	#print canvas['width'], canvas['height'], canvas['confine']
	#print canvas.winfo_width (), canvas.winfo_height ()
	
	canvas.r2cx = rx
	canvas.r2cy = ry

def hide_algorithm ():
	return master.show_var.get () != 0

################### ANDREW E EDUARDO MUDARAM #######################
def plot_circle (x, y, color, r):
	plot_id = canvas.create_oval (canvas.r2cx(x-r), canvas.r2cy(y-r),
	canvas.r2cx(x+r), canvas.r2cy(y+r), outline=color)
	return plot_id
def plot_curve (xy, color, linewidth):
	canvas_xy = []
	for i in range(len(xy)//2):
		canvas_xy += [canvas.r2cx(xy[i]), canvas.r2cy(xy[i+1])]
	lineto_id = canvas.create_line (canvas_xy, fill=color, width=linewidth)
	return lineto_id

####################################################################

######################## EDUARDO FREIRE ######################
def plot_disc_grande (x, y, color, r):
	plot_id = canvas.create_oval (canvas.r2cx(x - r), canvas.r2cy(y - r), 
					canvas.r2cx(x + r), canvas.r2cy(y + r), fill=color, outline = 'white')
	return plot_id
#############################################3


################ GERMANO & ANDRE ######################

def plot_vert_ray (x0, y0, increasing, color, linewidth):
	if not increasing:
		lineto_id = canvas.create_line (canvas.r2cx(x0), canvas.r2cy(y0), 
						canvas.r2cx(x0), int (canvas['height']), 
						fill=color, width=linewidth)
	else:
		lineto_id = canvas.create_line (canvas.r2cx(x0), canvas.r2cy(y0), 
						canvas.r2cx(x0), 0, 
						fill=color, width=linewidth)	
	return lineto_id

def plot_horiz_ray (x0, y0, increasing, color, linewidth):
	if increasing:
		lineto_id = canvas.create_line (canvas.r2cx(x0), canvas.r2cy(y0), 
						int (canvas['width']), canvas.r2cy(y0),
						fill=color, width=linewidth)
	else:
		lineto_id = canvas.create_line (canvas.r2cx(x0), canvas.r2cy(y0), 
						0, canvas.r2cy(y0), 
						fill=color, width=linewidth)	
	return lineto_id

################################################

