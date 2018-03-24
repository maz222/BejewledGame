import pygame

class Cursor:
	#horizontalN - the length of the row the cursor can move through (eg: [][][] = 3)
	#verticalN - the length of the column the cursor can move through

	#position - [row, col]!!!
	def __init__(self,horizontalN,verticalN,position=[0,0]):
		self.position = position
		self.horizontalN = horizontalN
		self.verticalN = verticalN
		self.width = 60
		self.height = 60

	def moveLeft(self):
		self.position[1] = (self.position[1] - 1) % self.horizontalN

	def moveRight(self):
		self.position[1] = (self.position[1] + 1) % self.horizontalN

	def moveUp(self):
		self.position[0] = (self.position[0] - 1) % self.verticalN

	def moveDown(self):
		self.position[0] = (self.position[0] + 1) % self.verticalN

	def move(self, key):
		if key == pygame.K_UP:
			self.moveUp()
		if key == pygame.K_DOWN:
			self.moveDown()
		if key == pygame.K_LEFT:
			self.moveLeft()
		if key == pygame.K_RIGHT:
			self.moveRight()

	def draw(self, screen, position, scale=1):
		pygame.draw.rect(screen, (0,0,0), (position[0],position[1], self.width*scale, self.height*scale), 3 * scale)