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

	#factor - float -1 -> 1 
	def scale(self, factor):
		if factor > 1 or factor < -1:
			raise ValueError("Scale factor must be -1 (-100%) to 1 (+100%")
		transMat = SimpleMat([(1+factor, 0), (0, 1+factor)])
		self.matrix = transMat * self.matrix

	#factor - angle to be rotated around origin
	def rotate(self, factor):
		factor = factor % 360
		factor = math.radians(factor)
		transMat = SimpleMat([(math.cos(factor),math.sin(factor)), (-math.sin(factor),math.cos(factor))])
		self.matrix = transMat * self.matrix

	#factor - angle to be rotated
	#Rotates IN PLACE ; around the center of the polygon
	def rotateSelf(self, factor):
		centerX = 0
		centerY = 0
		for point in self.matrix.cols:
			centerX += point[0]
			centerY += point[1]
		centerX /= len(self.matrix.cols)
		centerY /= len(self.matrix.cols)
		print(centerX, centerY)
		tempPoints = []
		for point in self.matrix.cols:
			tempPoint = (point[0] - centerX, point[1] - centerY)
			tempPoints.append(tempPoint)
		tempPoly = SimplePoly(tempPoints)
		#print(tempPoly)
		tempPoly.rotate(factor)
		#print(tempPoly)
		self.matrix += tempPoly.matrix

	def __str__(self):
		return str(self.matrix)

testPoly = SimplePoly([(0,0),(100,0),(100,100),(0,100)])
print(testPoly)
testPoly.rotateSelf(90)
print(testPoly)

