class SimpleMat:
	def __init__(self, cols):
		self.cols = []
		self.rowCount = len(cols[0])
		self.colCount = len(cols)
		for col in cols:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
			if len(col) != self.rowCount:
				raise ValueError("Wrong col length")
			self.cols.append(col)

	def __add__(self,matrix):
		if self.rowCount != matrix.rowCount or self.colCount != matrix.colCount:
			raise ValueError("Wrong matrix dimensions")
		temp = []
		for rowIndex, row in enumerate(self.cols):
			temp.append([])
			for i in range(len(row)):
				temp[rowIndex].append(row[i] + matrix.cols[rowIndex][i])
		return SimpleMat(temp)

	def __mul__(self,matrix):
		if self.colCount != matrix.rowCount:
			print(self)
			print(matrix)
			raise ValueError("Wrong matrix dimensions!")
		temp = []
		for col in matrix.cols:
			temp.append([])
			#multiply V-col vs self.row
			for i in range(len(col)):
				total = 0
				#multiple self.row val vs V-col val
				for j in range(len(col)):
					total += col[j] * self.cols[j][i]
				temp[len(temp)-1].append(total)
		return SimpleMat(temp)

	def __str__(self):
		return str(self.cols)

import math
class SimplePoly:
	def __init__(self, points):
		self.matrix = SimpleMat(points)

	def getPoints(self):
		points = []
		for point in self.matrix.cols:
			points.append(point)
		return points

	def scale(self, factor):
		transMat = SimpleMat([(factor, 0), (0, factor)])
		self.matrix = transMat * self.matrix

	def shearX(self, factor):
		transMat = SimpleMat([(1,0),(factor,1)])
		self.matrix = transMat * self.matrix

	def shearY(self, factor):
		transMat = SimpleMat([(1,factor),(0,1)])
		self.matrix = transMat * self.matrix

	#factor - angle to be rotated around origin
	def rotateAroundOrigin(self, factor):
		factor = factor % 360
		factor = math.radians(factor)
		transMat = SimpleMat([(math.cos(factor),-math.sin(factor)), (math.sin(factor),math.cos(factor))])
		self.matrix = transMat * self.matrix

	def rotateAroundPoint(self, point, factor):
		for i in range(self.matrix.colCount):
			self.matrix.cols[i] = (self.matrix.cols[i][0] - point[0], self.matrix.cols[i][1] - point[1])
		self.rotateAroundOrigin(factor)
		for i in range(self.matrix.colCount):
			self.matrix.cols[i] = (self.matrix.cols[i][0] + point[0], self.matrix.cols[i][1] + point[1])

	def getCenter(self):
		centerX = 0
		centerY = 0
		for point in self.matrix.cols:
			centerX += point[0]
			centerY += point[1]
		centerX /= self.matrix.colCount
		centerY /= self.matrix.colCount
		return (centerX, centerY)		

	def rotateSelf(self, factor):
		self.rotateAroundPoint(self.getCenter(), factor)

	def scaleInPlace(self, factor):
		center = self.getCenter()
		for i in range(self.matrix.colCount):
			self.matrix.cols[i] = (self.matrix.cols[i][0] - center[0], self.matrix.cols[i][1] - center[1])
		self.scale(factor)
		for i in range(self.matrix.colCount):
			self.matrix.cols[i] = (self.matrix.cols[i][0] + center[0], self.matrix.cols[i][1] + center[1])

	def __str__(self):
		return str(self.matrix)

import copy
import math
class BlockPoly:
	#origin = TOP LEFT CORNER
	def __init__(self, origin, width, height):
		self.origin = origin
		points = [origin,(origin[0]+width,origin[1]),(origin[0]+width,origin[1]+width),(origin[0],origin[1]+width)]
		self.basePoly = SimplePoly(points)
		self.currentPoly = SimplePoly(points)

	def updateOrigin(self, newOrigin):
		#print("old: " + str(self.origin) + " new: " + str(newOrigin))
		basePoints = self.basePoly.getPoints()
		for i in range(len(basePoints)):
			basePoints[i] = (basePoints[i][0] - self.origin[0] + newOrigin[0], basePoints[i][1] - self.origin[1] + newOrigin[1])
		currPoints = self.currentPoly.getPoints()
		for i in range(len(currPoints)):
			currPoints[i] = (currPoints[i][0] - self.origin[0] + newOrigin[0], currPoints[i][1] - self.origin[1], newOrigin[1])
		self.basePoly = SimplePoly(basePoints)
		self.currentPoly = SimplePoly(currPoints)
		self.origin = newOrigin

	def reset(self):
		#self.currentPoly = copy.deepcopy(self.basePoly)
		currPoints = self.currentPoly.getPoints()
		currDistance = math.sqrt((currPoints[0][0] - currPoints[3][0])**2 + (currPoints[0][1] - currPoints[3][1])**2)
		basePoints = self.basePoly.getPoints()
		baseDistance = math.sqrt((basePoints[0][0] - basePoints[3][0])**2 + (basePoints[0][1] - basePoints[3][1])**2)
		difference = 1 + (baseDistance - currDistance) / currDistance
		self.scaleBy(difference)

	#broken?
	def scaleTo(self, factor):
		self.reset()
		self.currentPoly.scaleInPlace(factor)

	def scaleBy(self, factor):
		self.currentPoly.scaleInPlace(factor)

	#broken
	def rotateTo(self, angle):
		self.reset()
		self.currentPoly.rotateSelf(angle)

	def rotateBy(self, angle):
		self.currentPoly.rotateSelf(angle)

	def rotateAroundPoint(self, point, angle):
		self.currentPoly.rotateAroundPoint(point, angle)

	def getPoints(self):
		return self.currentPoly.getPoints()