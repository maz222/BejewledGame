from BaseBlock import BaseBlock

from Cursor import Cursor

import random

class ColorGrid:

		# 0 = empty cell
		# 1 - 4 = color cell

		# (n) by (n) grid
		def __init__(self,n):
			self.grid = []
			for i in range(n):
				self.grid.append([])
				for j in range(n):
					self.grid[i].append(BaseBlock(random.randint(1,4)))

			#cursor set to (0,0) on the grid
			self.cursor = Cursor(n,n)

		def moveCursor(self, key):
			self.cursor.move(key)

		def deleteBlock(self):
			self.grid[self.cursor.position[1]][self.cursor.position[0]] = None

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
			#(row, col)
			#(1,0) (1,1)
			#(0,0) (0,1)
			for col in range(len(self.grid)):
				for row in range(len(self.grid)):
					#empty cell
					if self.grid[row][col] == None:
						toMove = []
						for up in range(row+1,len(self.grid)):
							if self.grid[up][col] != None:
								toMove.append((up,col))
						for index, cellIndex in enumerate(toMove):
							tempCell = self.grid[cellIndex[0]][cellIndex[1]]
							self.grid[cellIndex[0]][cellIndex[1]] = None
							self.grid[row+index][col] = tempCell

		def getEmptyCells(self):
			emptyCellList = []
			for row in range(len(self.grid)):
				for col in range(len(self.grid)):
					if self.grid[row][col] == None:
						emptyCellList.append((row,col))
			return emptyCellList

		def spawnNewCells(self, emptyCells):
			for cell in emptyCells:
				self.grid[cell[0]][cell[1]] = BaseBlock(random.randint(1,4))

		def clearLoop(self):
			matches = self.getMatches(3)
			if len(matches) == 0:
				return
			while len(matches) > 0:
				self.removeMatches(matches)
				self.moveCellsDown()
				matches = self.getMatches(3)
			#self.spawnNewCells()
			self.clearLoop()

		def draw(self, screen, position, scale=1):
			cellHeight = 50
			cellWidth = 50
			padding = 10
			for row in range(len(self.grid)-1,-1,-1):
				for col, cell in enumerate(self.grid[row]):
					cellPos = ((position[0] + col * (cellWidth + padding)), (position[1] + len(self.grid) * (cellHeight + padding) - (row + 1) * (cellHeight + padding)))
					if cell != None:
						if [col,row] != self.cursor.position:
							cell.draw(screen, cellPos)
						else:
							cellPos = (cellPos[0] + cellWidth*.25/2, cellPos[1] + cellHeight*.25/2)
							cell.draw(screen, cellPos, .75)
			cursorX = position[0] + self.cursor.position[0] * (cellWidth + padding) - ((self.cursor.width - cellWidth) / 2)
			cursorY = position[1] + len(self.grid) * (cellHeight + padding) - (self.cursor.position[1] + 1) * (cellHeight + padding) - ((self.cursor.height - cellHeight)/2)
			self.cursor.draw(screen, (cursorX, cursorY))

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