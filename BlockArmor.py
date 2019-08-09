import pygame

from SimpleVector import BlockPoly
from SimpleVector import SimpleMat

class BlockArmor:
	def __init__(self, position, width, height, thickness, health=1):
		self.health = health
		self.position = SimpleMat([position])
		self.height = height
		self.width = width
		self.thickness = thickness
		#self.poly = self.createPoly(position, width, height, thickness)
		self.poly = BlockPoly(position, width, height)

	def updatePosition(self, newPosition):
		self.position = SimpleMat([newPosition])
		self.poly = BlockPoly(self.position.cols[0], self.width, self.height)
		#self.poly.updateOrigin(self.position)

	def getPosition(self):
		return self.position.cols[0]

	def reduceHealth(self):
		self.health -= 1
		if self.health <= 0:
			return True
		return False

	def getHealth(self):
		return self.health

	def draw(self, screen, offset=(0,0)):
		color = (0,0,0)
		points = self.poly.getPoints()
		for i in range(len(points)):
			points[i] = (points[i][0] + offset[0], points[i][1] + offset[1])
		pygame.draw.polygon(screen, color, points)