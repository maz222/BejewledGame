import pygame
import math

from SimpleVector import BlockPoly
from SimpleVector import SimpleMat

colorDict = {1:"#B3411E", 2:"#90B31E", 3:"#1E90B3", 4:"#411EB3"}

class BaseBlock:

	#color = int (1-4)
		# 1 - #B3411E
		# 2 - #90B31E
		# 3 - #1E90B3
		# 4 - #411EB3

	#position = top left corner of block (in pixels) [x,y]
	
	def __init__(self, color, position, width, height):
		self.color = color
		self.isMoveable = True
		self.position = SimpleMat([position])
		self.poly = BlockPoly(position, width, height)
		self.width = width
		self.height = height

	def getColor(self):
		return self.color

	def getPosition(self):
		return self.position.cols[0]

	def updatePosition(self, newPosition):
		self.position = SimpleMat([newPosition])
		self.poly = BlockPoly(self.position.cols[0], self.width, self.height)
		#self.poly.updateOrigin(self.position)

	def rotate(self, clockWise):
		return

	def rotateAroundPoint(self, factor, point):
		#point = (-point[0],-point[1])
		#self.position += SimpleMat([point])
		#factor = factor % 360
		#factor = math.radians(factor)
		#transMat = SimpleMat([(math.cos(factor),-math.sin(factor)),(math.sin(factor),math.cos(factor))])
		#self.position = transMat * self.position
		#point = (-point[0],-point[1])
		#update position
		#self.position += SimpleMat([point])
		#self.poly = BlockPoly(self.position.cols[0], 50, 50)
		self.poly.rotateAroundPoint(point, factor)

	def rotateInPlace(self, factor):
		self.poly.rotateBy(factor)

	def scale(self, factor):
		self.poly.scaleTo(factor)

	#offset = (x,y) for uper left corner of the grid
	def draw(self, screen, offset=(0,0)):
		hexColor = colorDict[self.color].lstrip("#")
		rgbColor = tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))
		points = self.poly.getPoints()
		for i in range(len(points)):
			points[i] = (points[i][0] + offset[0], points[i][1] + offset[1])
		pygame.draw.polygon(screen, rgbColor, points)

	def __str__(self):
		return str(self.color)