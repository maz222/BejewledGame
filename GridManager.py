from BaseBlock import BaseBlock

from Cursor import Cursor

import random

cellHeight = 50
cellWidth = 50
padding = 10

class ColorGrid:

		# None = empty cell
		# 1 - 4 = color cell

		# (n) by (n) grid
		def __init__(self,n):

			self.grid = []
			for i in range(n):
				self.grid.append([])
				for j in range(n):
					cellPos = (j * (cellWidth + padding), i * (cellHeight + padding))
					self.grid[i].append(BaseBlock(random.randint(1,4), cellPos))

			#cursor set to (0,0) on the grid
			self.cursor = Cursor(n,n,[n-1,0])

		#coord - (row,col)
		def getCell(self, coord):
			return self.grid[coord[0]][coord[1]]

		#A / B = (row,col) of desired cells
		def swapCells(self, A, B):
			temp = self.grid[A[0]][A[1]]
			self.grid[A[0]][A[1]] = self.grid[B[0]][B[1]]
			self.grid[B[0]][B[1]] = temp
			cellA = self.grid[A[0]][A[1]]
			cellB = self.grid[B[0]][B[1]]
			if cellA != None:
				cellA.updatePosition((A[1] * (cellWidth + padding), A[0] * (cellHeight + padding)))
			if cellB != None:
				cellB.updatePosition((B[1] * (cellWidth + padding), B[0] * (cellHeight + padding)))

		def moveCursor(self, key):
			self.cursor.move(key)

		def deleteBlock(self):
			self.grid[self.cursor.position[0]][self.cursor.position[1]] = None

		def getVerticalMatches(self, minMatchLength):
			matchList = []
			#check bottom -> top
			for col in range(len(self.grid)):
				matchStack = []
				for row in range(len(self.grid)):
					cell = self.grid[row][col]
					if cell != None:
						if len(matchStack) == 0 or cell.getColor() == self.grid[matchStack[0][0]][matchStack[0][1]].getColor():
							matchStack.append((row,col))
						else:
							if len(matchStack) >= minMatchLength:
								matchList.append(matchStack)
							matchStack = [(row, col)]
					else:
						if len(matchStack) >= minMatchLength:
							matchList.append(matchStack)
						matchStack = []
				if len(matchStack) >= minMatchLength:
					matchList.append(matchStack)
			return matchList

		def getHorizontalMatches(self, minMatchLength):			
			matchList = []
			#check L -> R
			for rowIndex, rowList in enumerate(self.grid):
				matchStack = []
				for cellIndex, cell in enumerate(rowList):
					if cell != None:
						if len(matchStack) == 0 or cell.getColor() == self.grid[matchStack[0][0]][matchStack[0][1]].getColor():
							matchStack.append((rowIndex, cellIndex))
						else:
							if len(matchStack) >= minMatchLength:
								matchList.append(matchStack)
							matchStack = [(rowIndex, cellIndex)]
					else:
						if len(matchStack) >= minMatchLength:
							matchList.append(matchStack)
						matchStack = []
				if len(matchStack) >= minMatchLength:
					matchList.append(matchStack)
			return matchList

		def getMatches(self, minMatchLength):
			return self.getHorizontalMatches(minMatchLength) + self.getVerticalMatches(minMatchLength)

		def removeMatches(self, matchList):
			for matchSet in matchList:
				for matchCell in matchSet:
					self.grid[matchCell[0]][matchCell[1]] = None

		def moveCellsDown(self):
			colList = []
			for col in range(len(self.grid)):
				emptyStack = []
				toMove = []
				for row in range(len(self.grid)-1,-1,-1):
					if self.grid[row][col] == None:
						emptyStack.append((row,col))
					else:
						if self.grid[row][col].isMoveable and len(emptyStack) > 0:
							toMove.append(((row,col),emptyStack.pop(0)))
							emptyStack.append((row,col))
						if self.grid[row][col].isMoveable == False:
							emptyStack = []
				if len(toMove) > 0:
					colList.append(toMove)
			if len(colList) > 0:
				return colList
			return None

		def getEmptyCells(self):
			emptyCellList = []
			for row in range(len(self.grid)):
				for col in range(len(self.grid)):
					if self.grid[row][col] == None:
						emptyCellList.append((row,col))
			return emptyCellList

		def spawnNewCells(self, emptyCells):
			for cell in emptyCells:
				self.grid[cell[0]][cell[1]] = BaseBlock(random.randint(1,4),(cell[1] * (cellWidth + padding), cell[0] * (cellHeight + padding)))

		#modBlocks - a dictionary of block coordinates (row,col) for blocks that are rendered with...
		#modifier - a function that is called on each block (see above) that alters how it is rendered
		def draw(self, screen, position, modifier=None, modBlockCoords=None, *modifierParams):
			for row in range(len(self.grid)):
				for col in range(len(self.grid)):
					if self.grid[row][col] != None:
						if modifier != None:
							if modBlockCoords.get((row,col)) != None:
								modifier(self.grid[row][col], *modifierParams)
						self.grid[row][col].draw(screen, position)
			cursorX = self.cursor.position[1] * (cellWidth + padding) - (abs(cellWidth - self.cursor.width))/2
			cursorY = self.cursor.position[0] * (cellHeight + padding) - (abs(cellHeight - self.cursor.height))/2
			self.cursor.draw(screen, (position[0] + cursorX, position[1] + cursorY))

		def __str__(self):
			outStr = ""
			for i in range(len(self.grid)):
				for cell in self.grid[i]:
					cellStr = str(cell)
					if cell == None:
						cellStr = "0"
					for j in range(len(cellStr),3):
						cellStr += " "
					outStr += cellStr + " "
				outStr += "\n"
			return outStr