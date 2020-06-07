class Vertex:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.visited = False

	def getVisited(self):
		return self.visited

	def setVisited(self, value):
		self.visited = value

	def getX(self):
		return self.x

	def getY(self):
		return self.y

	def getPrev(self):
		return self.prev

	def setPrev(self, v):
		self.prev = v