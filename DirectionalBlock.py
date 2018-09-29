from BaseBlock import BaseBlock

from SimpleVector import SimplePoly
from SimpleVector import SimpleMat

import math
import pygame

colorDict = {1:"#B3411E", 2:"#90B31E", 3:"#1E90B3", 4:"#411EB3"}


class DirectionalBlock(BaseBlock):
	#colors - [top color, right color, bottom color, left color] (clockwise!)
		#color = int (1-4)
		# 1 - #B3411E
		# 2 - #90B31E
		# 3 - #1E90B3
		# 4 - #411EB3

	#position = top left corner of block (in pixels) [x,y]
	def createPoly(self, position):
		width = self.width
		height = self.height
		p = position
		topLeft = (p[0],p[1])
		topRight = (p[0]+width,p[1])
		bottomRight = (p[0]+width,p[1]+height)
		bottomLeft = (p[0],p[1]+height)
		center = (p[0]+width/2,p[1]+height/2)
		topPoly = [topLeft,topRight,center]
		rightPoly = [topRight,bottomRight,center]
		bottomPoly = [bottomRight, bottomLeft, center]
		leftPoly = [bottomLeft, topLeft, center]
		polys = [SimplePoly(topPoly),SimplePoly(rightPoly),SimplePoly(bottomPoly),SimplePoly(leftPoly)]
		return polys

	def __init__(self, colors, position, width, height):
		self.colors = colors
		self.position = SimpleMat([position])
		self.isMoveable = True
		self.width = width
		self.height = height
		self.polys = self.createPoly(position)

	def rotateColorsClockwise(self):
		tempA = self.colors[0]
		for i in range(len(self.colors)):
			tempB = self.colors[(i+1)%len(self.colors)]
			self.colors[(i+1)%len(self.colors)] = tempA
			tempA = tempB

	def rotateColorsCounterClockwise(self):
		tempA = self.colors[0]
		for i in range(len(self.colors)):
			tempB = self.colors[len(self.colors)-1-i]
			self.colors[len(self.colors)-1-i] = tempA
			tempA = tempB

	#returns the *top* color
	def getColor(self):
		return self.colors[0]

	def updatePosition(self, newPosition):
		self.position = SimpleMat([newPosition])
		self.polys = self.createPoly(newPosition)

	def rotate(self, clockWise):
		super().rotate(clockWise)
		if clockWise:
			self.rotateColorsClockwise()
		else:
			self.rotateColorsCounterClockwise()

	def rotateAroundPoint(self, factor, point):
		for p in self.polys:
			p.rotateAroundPoint(point, factor)

	def rotateInPlace(self, factor):
		for p in self.polys:
			#p.rotateSelf(factor)
			center = (self.getPosition()[0]+self.width/2,
				self.getPosition()[1]+self.height/2)
			p.rotateAroundPoint(center,factor)

	def scale(self, factor):
		for p in self.polys:
			#p.scaleTo(factor)
			p.scaleInPlace(factor)
			if factor > 1:
				distance = math.sqrt((0-25)**2 + (0-25)**2) * (factor - 1)
				#p.moveBy((distance*-1,distance*-1))
			else:
				distance = math.sqrt((0-25)**2 + (0-25)**2) * (1 - factor)
				#p.moveBy((distance,distance))

	def draw(self, screen, offset=(0,0)):
		for i in range(len(self.colors)):
			hexColor = colorDict[self.colors[i]].lstrip("#")
			rgbColor = tuple(int(hexColor[i:i+2], 16) for i in (0, 2 ,4))
			points = self.polys[i].getPoints()
			for j in range(len(points)):
				points[j] = (points[j][0] + offset[0], points[j][1] + offset[1])
			pygame.draw.polygon(screen, rgbColor, points)

	def __str__(self):
		return str(self.colors)	