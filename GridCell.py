from BaseBlock import BaseBlock
from BlockArmor import BlockArmor

class GridCellContainer:
	def __init__(self, block, blockArmor=None):
		self.block = block
		self.blockArmor = blockArmor

		if blockArmor:
			thickness = self.blockArmor.thickness/2
			self.block.width -= thickness * 2
			self.block.height -= thickness * 2
			oldPosition = self.block.getPosition()
			newPosition = (oldPosition[0]+thickness,oldPosition[1]+thickness)
			self.block.updatePosition(newPosition)

	def rotateAroundPoint(self, factor, origin):
		self.block.rotateAroundPoint(origin, factor)
		if self.blockArmor:
			self.blockArmor.poly.rotateAroundPoint(origin, factor)

	def rotateInPlace(self, factor):
		self.block.rotateInPlace(factor)
		if self.blockArmor:
			self.blockArmor.poly.rotateBy(factor)

	def scale(self, factor):
		self.block.scale(factor)
		if self.blockArmor:
			self.blockArmor.poly.scaleTo(factor)

	def moveTo(self, newPosition):
		if self.blockArmor:
			self.blockArmor.updatePosition(newPosition)
			thickness = self.blockArmor.thickness/2
			temp = (newPosition[0]+thickness,newPosition[1]+thickness)
			self.block.updatePosition(temp)
		else:
			self.block.updatePosition(newPosition)

	def draw(self, screen, offset=(0,0)):
		if self.blockArmor:
			self.blockArmor.draw(screen, offset)
		self.block.draw(screen, offset)

	def getHP(self):
		if self.blockArmor:
			return self.blockArmor.getHealth()
		else:
			return 0

	def reduceHP(self):
		if self.blockArmor:
			self.blockArmor.reduceHealth()





