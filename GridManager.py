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
			#add second, empty grid
			for i in range(n):
				self.grid.append([])
				for j in range(n):
					self.grid[i].append(None)
			#create grid filled with blocks
			for i in range(n):
				self.grid.append([])
				for j in range(n):
					cellPos = (j * (cellWidth + padding), (n+i) * (cellHeight + padding))
					self.grid[n+i].append(BaseBlock(random.randint(1,4), cellPos))
			self.n = n
			self.center = (n*(cellWidth+padding)/2, n*(cellHeight+padding) + n*(cellHeight+padding)/2)

			#cursor set to (0,0) on the grid
			self.cursor = Cursor(n,n,[n-1,0])

		def rotateClock(self):
			for i in range(3):
				self.rotateCounter()			

		def rotateCounter(self):
			N = self.n
			for x in range(0, int(N/2)):
				for y in range(x, N-x-1):
					top = ((x+N),y)
					right = ((y+N),(N-1-x))
					bottom = ((N-1-x+N),(N-1-y))
					left = ((N-1-y+N),(x))
					self.swapCells(top, left)
					self.swapCells(top, bottom)
					self.swapCells(top, right)

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
			self.grid[self.cursor.position[0]+self.n][self.cursor.position[1]] = None

		def getVerticalMatches(self, minMatchLength):
			matchSet = set([])
			#check bottom -> top
			for col in range(self.n):
				matchStack = []
				#only check the bottom grid (n/2)
				for row in range(self.n-1,self.n*2,1):
					cell = self.grid[row][col]
					if cell != None:
						if len(matchStack) == 0 or cell.getColor() == self.grid[matchStack[0][0]][matchStack[0][1]].getColor():
							matchStack.append((row,col))
						else:
							if len(matchStack) >= minMatchLength:
								for cell in matchStack:
									matchSet.add(cell)
							matchStack = [(row, col)]
					else:
						if len(matchStack) >= minMatchLength:
							for cell in matchStack:
								matchSet.add(cell)
						matchStack = []
				if len(matchStack) >= minMatchLength:
					for cell in matchStack:
						matchSet.add(cell)
			return matchSet

		def getHorizontalMatches(self, minMatchLength):			
			matchSet = set([])
			#check L -> R
			#only check the bottom grid (n/2)
			for rowIndex in range(self.n-1,self.n*2,1):
				rowList = self.grid[rowIndex]
				matchStack = []
				for cellIndex, cell in enumerate(rowList):
					if cell != None:
						if len(matchStack) == 0 or cell.getColor() == self.grid[matchStack[0][0]][matchStack[0][1]].getColor():
							matchStack.append((rowIndex, cellIndex))
						else:
							if len(matchStack) >= minMatchLength:
								for cell in matchStack:
									matchSet.add(cell)
							matchStack = [(rowIndex, cellIndex)]
					else:
						if len(matchStack) >= minMatchLength:
							for cell in matchStack:
								matchSet.add(cell)
						matchStack = []
				if len(matchStack) >= minMatchLength:
					for cell in matchStack:
						matchSet.add(cell)
			return matchSet

		def getMatches(self, minMatchLength):
			return self.getHorizontalMatches(minMatchLength).union(self.getVerticalMatches(minMatchLength))

		def removeMatches(self, matchList):
			for matchCell in matchList:
				self.grid[matchCell[0]][matchCell[1]] = None

		def moveCellsDown(self):
			colList = []
			for col in range(self.n):
				emptyStack = []
				toMove = []
				for row in range(self.n*2-1,-1,-1):
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
			for col in range(self.n):
				for row in range(self.n,self.n*2,1):
					if self.grid[row][col] == None:
						emptyCellList.append((row,col))
					else:
						break
			return emptyCellList

		def spawnNewCells(self, emptyCells):
			for cell in emptyCells:
				self.grid[cell[0]-self.n][cell[1]] = BaseBlock(random.randint(1,4),(cell[1] * (cellWidth + padding), (cell[0]-self.n) * (cellHeight + padding)))

		def scaleCells(self, cellList, factor):
			for index in cellList:
				self.grid[index[0]][index[1]].scale(factor)

		def rotateCells(self, cellList, factor):
			for index in cellList:
				self.grid[index[0]][index[1]].rotateInPlace(factor)

		def rotateGrid(self, factor):
			for row in self.grid:
				for cell in row:
					if cell != None: 
						#cell.poly.rotateAroundPoint((85, 85+180),factor)
						cell.poly.rotateAroundPoint(self.center,factor)
						#cell.rotateAroundPoint(factor, self.center)


		def draw(self, screen, position):
			for row in range(self.n*2):
				for col in range(self.n):
					if self.grid[row][col] != None:
						self.grid[row][col].draw(screen, position)
			cursorX = self.cursor.position[1] * (cellWidth + padding) - (abs(cellWidth - self.cursor.width))/2
			cursorY = (self.cursor.position[0] + self.n) * (cellHeight + padding) - (abs(cellHeight - self.cursor.height))/2
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