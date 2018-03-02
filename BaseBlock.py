import pygame

colorDict = {1:"#B3411E", 2:"#90B31E", 3:"#1E90B3", 4:"#411EB3"}

class BaseBlock:

	#color = int (1-4)
		# 1 - #B3411E
		# 2 - #90B31E
		# 3 - #1E90B3
		# 4 - #411EB3
	
	def __init__(self, color):
		self.color = color
		self.isMoveable = True
		self.baseWidth = 50
		self.baseHeight = 50

	def getColor(self):
		return self.color

	#position = (x,y) for uper left corner
	def draw(self, screen, position, scale=1):
		hexColor = colorDict[self.color].lstrip("#")
		rgbColor = tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))
		pygame.draw.rect(screen, rgbColor, (position[0],position[1], self.baseWidth*scale, self.baseHeight*scale), 0)

	def __str__(self):
		return str(self.color)


