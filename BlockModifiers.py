import math

from BaseBlock import BaseBlock

class BlockModifiers:
	#first param is ALWAYS BLOCK

	@staticmethod
	#scale - float(-1 to 1)
			# -1 -> shrink block 100%
			#  1 -> grow block 100%
	def scaleBlock(block, scale):
		width = (block.width * scale) + block.width
		height =(block.height * scale) + block.height
		xOffset = (block.width - width) / 2
		#change the origin xCoordinate 
			#if block has grown, shift to the left, otherwise to the right (multiply by -1)
		xPos = block.position[0] + xOffset
		yOffset = (block.height - height) / 2
		yPos = block.position[1] + yOffset
		block.position = (xPos, yPos)
		block.width = width
		block.height = height

	@staticmethod
	#sets a block back to its base dimensions / scale
	def resetBlockScale(block):
		scaleDiff = ((block.width / block.baseWidth) - 1) * -1
		BlockModifiers.scaleBlock(scaleDiff, block)
