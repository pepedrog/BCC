from geocomp.common.polygon import Polygon
from geocomp.common.segment import Segment
from geocomp.common.point import Point
from geocomp.common.vertex import Vertex
from geocomp.common.edge import Edge
from geocomp.common import control

# Código extra para printar
def Printo(pol):
	pol.hilight()
	control.sleep()
	pol.plot('magenta')

class Graph:
	def __init__(self):
		self.allVertex = []
		self.allEdge   = []
		self.solved    = False

	# Cria um vertex no grafo
	def newVertex(self, x, y):
		self.allVertex.append(Vertex(x, y))
		Printo(Point(x, y))
	
	# Procura um vertex do grafo
	def findVertex(self, x, y):
		for i in self.allVertex:
			if (i.getX() == x) and (i.getY() == y):
				return i
		else:
			return None

	# Cria uma aresta no grafo
	def newEdge(self, x1, y1, x2, y2):
		vertex1 = self.findVertex(x1, y1)
		vertex2 = self.findVertex(x2, y2)
		if (vertex1 != None) and (vertex2 != None):
			self.allEdge.append(Edge(vertex1, vertex2))
			point1 = Point(vertex1.getX(), vertex1.getY())
			point2 = Point(vertex2.getX(), vertex2.getY())
			Printo(Segment(point1, point2))
		else:
			print("Falhou em newEdge -- vertices errados!")

	# Procura um vértice que ainda não foi visitado
	def findNeighbor(self, v):
		for i in range(len(self.allEdge)):
			start = self.allEdge[i].getStart()
			end   = self.allEdge[i].getEnd()
			if (v.getX() == start.getX()) and (v.getY() == start.getY()) and (end.getVisited() == False):
				end.setVisited(True)
				return end
			if (v.getX()==end.getX()) and (v.getY()==end.getY()) and (start.getVisited()==False):
				start.setVisited(True)
				return start
		return None

	# Algoritmo base do DFS
	def DFS(self, target, start):
		if (target.x == start.x and target.y == start.y):
			print("O robô chegou ao destino!")
		else:
			for v in self.allVertex:
				v.setVisited(False)
			if (self.visit(start, target) == 1):
				print("O robô chegou ao destino!")
			else:
				print("Falhou em visit -- não achou o caminho :(")

	# Funcao auxiliar do DFS
	def visit(self, u, target):
		u.setVisited(True)
		v = self.findNeighbor(u)
		while v is not None:

			# Printando o segmento atual do grafo
			seg = Segment(Point(u.x, u.y), Point(v.x, v.y))
			seg.plot('cyan')
			control.sleep()

			# Continuar o DFS
			if (v == target):
				self.solved = True
				return 1
			self.visit(v, target)

			# Condicao de parada do DFS
			if(self.solved):
				return 1

			# Retirando o print do segmento
			seg.hide()
			control.sleep()

			# Pegar o próximo vizinho
			v = self.findNeighbor(u)
