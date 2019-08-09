from BaseBlock import BaseBlock

from SimpleVector import BlockPoly

import pygame

colorDict = {1:"#B3411E", 2:"#90B31E", 3:"#1E90B3", 4:"#411EB3"}

class DirectionalBlock(BaseBlock):
	@staticmethod
	def getPoints(baseBlockPoly):
		center = baseBlockPoly.poly.getCenter()
		points = baseBlockPoly.getPoints()
		top = [points[0],points[1],center]
		right = [points[1],points[2],center]
		bottom = [points[2],points[3],center]
		left = [points[3],points[0],center]
		return [top,right,bottom,left]

	def __init__(self,colors,position,width,height):
		self.colors = colors
		super().__init__(colors[0],position,width,height)

	def rotate(self,clockWise=False):
		if clockWise:
			self.rotateColorsClockwise()
		else:
			self.rotateColorsCounterClockwise()

	def rotateColorsClockwise(self):
		tempA = self.colors[0]
		for i in range(len(self.colors)):
			tempB = self.colors[(i+1)%len(self.colors)]
			self.colors[(i+1)%len(self.colors)] = tempA
			tempA = tempB
		self.color = self.colors[0]

	def rotateColorsCounterClockwise(self):
		tempA = self.colors[0]
		for i in range(len(self.colors)):
			tempB = self.colors[len(self.colors)-1-i]
			self.colors[len(self.colors)-1-i] = tempA
			tempA = tempB	
		self.color = self.colors[0]

	def draw(self,screen,offset=(0,0)):
		points = DirectionalBlock.getPoints(self.poly)
		for s in range(len(points)):
			pSet = points[s]
			for p in range(len(pSet)):
				pSet[p] = (pSet[p][0] + offset[0],pSet[p][1] + offset[1])
			points[s] = pSet
		for i in range(len(self.colors)):
			hexColor = colorDict[self.colors[i]].lstrip("#")
			rgbColor = tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))
			pygame.draw.polygon(screen, rgbColor, points[i])