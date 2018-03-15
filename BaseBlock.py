import pygame

colorDict = {1:"#B3411E", 2:"#90B31E", 3:"#1E90B3", 4:"#411EB3"}

class BaseBlock:

	#color = int (1-4)
		# 1 - #B3411E
		# 2 - #90B31E
		# 3 - #1E90B3
		# 4 - #411EB3

	#position = top left corner of block (in pixels) [x,y]
	
	def __init__(self, color, position):
		self.color = color
		self.isMoveable = True
		self.baseWidth = 50
		self.width = self.baseWidth
		self.baseHeight = 50
		self.height = self.baseHeight
		self.position = position

	def getColor(self):
		return self.color

	def updatePosition(self, newPosition):
		#print("updating from: " + str(self.position) + " to: " + str(newPosition))
		self.position = newPosition

	#offset = (x,y) for uper left corner of the grid
	def draw(self, screen, offset):
		hexColor = colorDict[self.color].lstrip("#")
		rgbColor = tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))
		pygame.draw.rect(screen, rgbColor, (offset[0] + self.position[0],offset[1] + self.position[1], self.width, self.height), 0)

	def __str__(self):
		return str(self.color)


