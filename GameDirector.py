import pygame
import math

from BlockModifiers import BlockModifiers

cellHeight = 50
cellWidth = 50
padding = 10

#base/template state
class GameState:
   def __init__(self, gridManager):
      self.grid = gridManager
   def update(self, inputs):
      moveKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
      for event in inputs:
         if event.type == pygame.KEYDOWN:
            #move the target cursor around
            if event.key in moveKeys:
               self.grid.moveCursor(event.key)
   def draw(self, screen, gridPos):
      screen.fill((200,200,200))
      self.grid.draw(screen, gridPos)


#checks the grid for matches
   #Check -> Remove (matches found)
   #     -> Spawn (no matches)
class CheckState(GameState):
   def update(self, inputs):
      super().update(inputs)
      matches = self.grid.getMatches(3)
      if len(matches) > 0:
         return RemoveState(self.grid, matches)
      else:
         return SpawnState(self.grid)
         #return ReadyState(self.grid)

#removes matches from the grid
   #Remove -> Fall
class RemoveState(GameState):
   def __init__(self, gridManager, matches):
      self.matches = matches
      self.grid = gridManager
      self.shrinkScale = -.02
      self.currScale = 1
   def update(self, inputs):
      super().update(inputs)
      if self.currScale <= 0:
         self.grid.removeMatches(self.matches)
         return FallState(self.grid)
      else:
         self.currScale += self.shrinkScale
         self.grid.rotateCells(self.matches, 5)
         self.grid.scaleCells(self.matches, self.currScale)
      return self
   def draw(self, screen, gridPos):
      screen.fill((200,200,200))
      self.grid.draw(screen, gridPos)

#spawns new blocks into the grid
   #Spawn -> Fall (new blocks spawned)
   #      -> Ready (no new blocks spawned)
class SpawnState(GameState):
   def update(self, inputs):
      super().update(inputs)
      emptyCells = self.grid.getEmptyCells()
      if len(emptyCells) > 0:
         self.grid.spawnNewCells(emptyCells)
         return FallState(self.grid)
         #return CheckState(self.grid)
      else:
         return ReadyState(self.grid)

#main state - handles user input when game is "ready" to play
   #Ready -> Ready (no action taken)
   #      -> Fall (block was deleted by player)
class ReadyState(GameState):
   def update(self, inputs):
      moveKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
      for event in inputs:
         if event.type == pygame.KEYDOWN:
            #move the target cursor around
            if event.key in moveKeys:
               self.grid.moveCursor(event.key)
            elif event.key == pygame.K_r:
               print(self.grid)
            #delete a block from the grid, causing other blocks to fall
            elif event.key == pygame.K_DELETE:
               self.grid.deleteBlock()
               return FallState(self.grid)
      return self

gravity = .02
#moves block down
   #Fall -> Check
class FallState(GameState):
   def __init__(self, gridManager):
      self.grid = gridManager
      self.toMove = self.grid.moveCellsDown()
      self.blockSpeed = gravity
   def update(self, inputs):
      super().update(inputs)
      self.blockSpeed += gravity
      if self.toMove == None or len(self.toMove) == 0:
         return CheckState(self.grid)
      #iterate over a copy of the list so that you can alter/remove from it
      for col in list(self.toMove):
         for pair in list(col):
            block = self.grid.getCell(pair[0])
            targetPosition = (pair[1][1] * 60, pair[1][0] * 60)
            oldDistance = math.sqrt((targetPosition[0]-block.position[0])**2 + (targetPosition[1]-block.position[1])**2)
            xSlope = targetPosition[0] - block.position[0]
            ySlope = targetPosition[1] - block.position[1]
            newPos = (block.position[0] + self.blockSpeed*xSlope, block.position[1] + self.blockSpeed*ySlope)
            #newDistance = math.sqrt((targetPosition[0]-newPos[0])**2 + (targetPosition[1]-newPos[1])**2)
            # done moving
            if xSlope == 0 and ySlope == 0:
               self.grid.swapCells(pair[0],pair[1])
               col.remove(pair)
            else:
               block.updatePosition(newPos)
         if len(col) == 0:
            self.toMove.remove(col)
      return self


#state machine
class GameDirector:
   def __init__(self, gridManager):
      self.grid = gridManager
      self.currentState = ReadyState(self.grid)
   def update(self, inputs):
      self.currentState = self.currentState.update(inputs)
   def draw(self, screen):
      gridPos = ((1280/2 - self.grid.n*60/2),(720/2 - self.grid.n*60 - self.grid.n*60/2))
      self.currentState.draw(screen, gridPos)
