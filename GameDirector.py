import pygame
import math


cellHeight = 50
cellWidth = 50
padding = 10

#base/template state
class GameState:
   def __init__(self, gameData):
      self.gameData = gameData
   def update(self, inputs):
      grid = self.gameData["grid"]
      moveKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
      for event in inputs:
         if event.type == pygame.KEYDOWN:
            #move the target cursor around
            if event.key in moveKeys:
               grid.moveCursor(event.key)
   def draw(self, screen, gridPos):
      screen.fill((200,200,200))
      self.gameData["grid"].draw(screen, gridPos)

class RotateState(GameState):
   def __init__(self, gameData, clockWise=True):
      self.gameData = gameData
      self.totalAngle = 0
      self.clockWise = clockWise
   def update(self, inputs):
      grid = self.gameData["grid"]
      if self.clockWise:
         grid.rotateGrid(2)
      else:
         grid.rotateGrid(-2)
      self.totalAngle += 2
      if self.totalAngle >= 90:
         if not self.clockWise:
            grid.rotateClock()
         else:
            grid.rotateCounter()
         return CheckState(self.gameData)
      return self

#checks the grid for matches
   #Check -> Remove (matches found)
   #      -> Spawn (no matches)
class CheckState(GameState):
   def update(self, inputs):
      super().update(inputs)
      matches = self.gameData["grid"].getMatches(3)
      if len(matches) > 0:
         self.gameData["score"].addScore(len(matches))
         return RemoveState(self.gameData, matches)
      else:
         return SpawnState(self.gameData)

#removes matches from the grid
   #Remove -> Fall
class RemoveState(GameState):
   def __init__(self, gameData, matches):
      self.matches = matches
      self.gameData = gameData
      self.shrinkScale = -.04
      self.currScale = 1
   def update(self, inputs):
      super().update(inputs)
      grid = self.gameData["grid"]
      if self.currScale <= 0:
         grid.removeMatches(self.matches)
         return FallState(self.gameData)
      else:
         self.currScale += self.shrinkScale
         grid.rotateCells(self.matches, 10)
         grid.scaleCells(self.matches, self.currScale)
      return self

#spawns new blocks into the grid
   #Spawn -> Fall (new blocks spawned)
   #      -> Ready (no new blocks spawned)
class SpawnState(GameState):
   def update(self, inputs):
      super().update(inputs)
      emptyCells = self.gameData["grid"].getEmptyCells()
      if len(emptyCells) > 0:
         self.gameData["grid"].spawnNewCells(emptyCells)
         return FallState(self.gameData)
      else:
         return ReadyState(self.gameData)

#main state - handles user input when game is "ready" to play
   #Ready -> Ready (no action taken)
   #      -> Fall (block was deleted by player)
class ReadyState(GameState):
   def update(self, inputs):
      moveKeys = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
      for event in inputs:
         if event.type == pygame.KEYDOWN:
            #check for rotations
            if event.key == pygame.K_LEFT:
               keys = pygame.key.get_pressed()
               if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
                  return RotateState(self.gameData, False)
            elif event.key == pygame.K_RIGHT:
               keys = pygame.key.get_pressed()
               if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
                  return RotateState(self.gameData, True)
            #move the target cursor around
            if event.key in moveKeys:
               self.gameData["grid"].moveCursor(event.key)
            #delete a block from the grid, causing other blocks to fall
            elif event.key == pygame.K_DELETE:
               self.gameData["grid"].deleteBlock()
               return FallState(self.gameData)
      return self

gravity = .04
#moves block down
   #Fall -> Check
class FallState(GameState):
   def __init__(self, gameData):
      self.gameData = gameData
      self.toMove = self.gameData["grid"].moveCellsDown()
      self.blockSpeed = gravity
   def update(self, inputs):
      super().update(inputs)
      self.blockSpeed += gravity
      if self.toMove == None or len(self.toMove) == 0:
         return CheckState(self.gameData)
      #iterate over a copy of the list so that you can alter/remove from it
      for col in list(self.toMove):
         for pair in list(col):
            block = self.gameData["grid"].getCell(pair[0])
            targetPosition = (pair[1][1] * 60, pair[1][0] * 60)
            oldDistance = math.sqrt((targetPosition[0]-block.getPosition()[0])**2 + (targetPosition[1]-block.getPosition()[1])**2)
            xSlope = targetPosition[0] - block.getPosition()[0]
            ySlope = targetPosition[1] - block.getPosition()[1]
            newPos = (block.getPosition()[0] + self.blockSpeed*xSlope, block.getPosition()[1] + self.blockSpeed*ySlope)
            #newDistance = math.sqrt((targetPosition[0]-newPos[0])**2 + (targetPosition[1]-newPos[1])**2)
            # done moving
            if xSlope == 0 and ySlope == 0:
               self.gameData["grid"].swapCells(pair[0],pair[1])
               col.remove(pair)
            else:
               block.updatePosition(newPos)
         if len(col) == 0:
            self.toMove.remove(col)
      return self

from GridManager import ColorGrid
from BaseBlock import BaseBlock
from ScoreKeeper import ScoreKeeper

#state machine
#gameData:
   #["grid"]-gridManager
   #["score"]-scoreKeeper
class GameDirector:
   def __init__(self, gridSize=7):
      score = ScoreKeeper()
      grid = ColorGrid(gridSize)
      gameData = {}
      gameData["grid"] = grid
      gameData["score"] = score
      self.gameData = gameData
      self.currentState = ReadyState(gameData)
   def update(self, inputs):
      self.currentState = self.currentState.update(inputs)
   def draw(self, screen):
      grid = self.gameData["grid"]
      gridPos = ((1280/2 - grid.n*60/2),(720/2 - grid.n*60 - grid.n*60/2))
      self.currentState.draw(screen, gridPos)
      self.gameData["score"].draw(screen)
