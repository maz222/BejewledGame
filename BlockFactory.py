from GameConstants import GameConstants

from GridCell import GridCellContainer

from BaseBlock import BaseBlock
from DirectionalBlock import DirectionalBlock
from BlockArmor import BlockArmor

import random

class BlockFactory:
	def __init__(self, time=0):
		self.time = time
		self.gameData = GameConstants.instance()
	def update(self):
		self.time += 1

	def build(self,position):
		blockChance = random.randint(0,100)
		armor = None
		if blockChance < 85:
			block = self.getBasicBlock(position)
			armorChance = random.randint(0,100)
			if armorChance >= 85:
				armor = self.getBlockArmor(position)
		else:
			directionChance = random.randint(0,100)
			if directionChance >= 50:
				if directionChance >= 75:
					block = self.get2SideDirectionalBlock(position)
				else:
					block = self.get2CornerDirectionalBlock(position)
			else:
				block = self.get4DirectionalBlock(position)
			armorChance = random.randint(0,100)
			if armorChance >= 90:
				armor = self.getBlockArmor(position)
		return GridCellContainer(block,armor)

	def getBlockConstants(self):
		return [self.gameData.get("blockColors")[:],
				self.gameData.get("cellWidth"),
				self.gameData.get("cellHeight")]

	def getBlockArmor(self,position,health=1):
		blockData = self.getBlockConstants()
		return BlockArmor(position,blockData[1],blockData[2],
				self.gameData.get("armorThickness"))

	def getBasicBlock(self,position):
		blockData = self.getBlockConstants()
		k = random.randint(0,len(blockData[0])-1)
		color = blockData[0][k]
		return BaseBlock(color,position,blockData[1],blockData[2])
	def get4DirectionalBlock(self,position):
		blockData = self.getBlockConstants()
		colors = []
		while len(colors) < 4:
			i = random.randint(0,len(blockData[0])-1)
			colors.append(blockData[0].pop(i))
		return DirectionalBlock(colors,position,blockData[1],blockData[2])
	def get2SideDirectionalBlock(self,position):
		blockData = self.getBlockConstants()
		colors = [0 for i in range(4)]
		for i in range(2):
			k = random.randint(0,len(blockData[0])-1)
			c = blockData[0].pop(k)
			colors[i] = c
			colors[i+2] = c
			print()
		return DirectionalBlock(colors,position,blockData[1],blockData[2])
	def get2CornerDirectionalBlock(self,position):
		blockData = self.getBlockConstants()
		colors = []
		for i in range(2):
			k = random.randint(0,len(blockData[0])-1)
			c = blockData[0].pop(k)
			colors.append(c)
			colors.append(c)
		return DirectionalBlock(colors,position,blockData[1],blockData[2])




