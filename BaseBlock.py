import pygame

from SimpleVector import BlockPoly

colorDict = {1:"#B3411E", 2:"#90B31E", 3:"#1E90B3", 4:"#411EB3"}

class BaseBlock:

	#color = int (1-4)
		# 1 - #B3411E
		# 2 - #90B31E
		# 3 - #1E90B3
		# 4 - #411EB3

	#position = top left corner of block (in pixels) [x,y]
	
	def __init__(self, color, position, width=50, height=50):
		self.color = color
		self.isMoveable = True
		self.position = position
		self.poly = BlockPoly(self.position, width, height)

	def getColor(self):
		return self.color

	def updatePosition(self, newPosition):
		self.position = newPosition
		self.poly = BlockPoly(self.position, 50, 50)
		#self.poly.updateOrigin(self.position)

	#offset = (x,y) for uper left corner of the grid
	def draw(self, screen, offset):
		hexColor = colorDict[self.color].lstrip("#")
		rgbColor = tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))
		points = self.poly.getPoints()
		for i in range(len(points)):
			points[i] = (points[i][0] + offset[0], points[i][1] + offset[1])
		pygame.draw.polygon(screen, rgbColor, points)

	def __str__(self):
		return str(self.color)