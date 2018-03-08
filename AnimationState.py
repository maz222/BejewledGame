import GameDirector
#moves block down
   #Fall -> Check
class FallState(GameDirector.GameState):
	gravity = .01
	def __init__(self, gridManager):
		self.grid = gridManager
		self.toMove = self.grid.moveCellsDown()
		self.blockSpeed = gravity
	def update(self, inputs):
		if len(self.toMove) == 0:
			return GameDirector.CheckState(self.grid)
		#iterate over a copy of the list so that you can alter/remove from it
		for pair in list(self.toMove):
			block = self.grid[pair[0][0]][pair[0][1]]
			targetPosition = (pair[1][1]*block.blockWidth, pair[1][0]*block.blockHeight)
			oldDistance = sqrt((targetPosition[0]-block.position[0])**2 + (targetPosition[1]-block.position[1])**2)
			xSlope = targetPosition[0] - block.position[0]
			ySlope = targetPosition[1] - block.position[1]
			newPos = (block.position[0] + self.blockSpeed*xSlope, block.position[1] + self.blockSpeed*ySlope)
			newDistance = sqrt((targetPosition[0]-newPos[0])**2 + (targetPosition[1]-newPos[1])**2)
			#overshot - done moving
			if newDistance > oldDistance:
				self.grid.swapCells(pair[0],pair[1])
				self.toMove.remove(pair)
			else:
				block.position = newPos