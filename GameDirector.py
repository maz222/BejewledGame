import pygame

#base/template state
class GameState:
   def __init__(self, gridManager):
      self.grid = gridManager
   def update(self, inputs):
      pass


#checks the grid for matches
   #Check -> Remove (matches found)
   #     -> Spawn (no matches)
class CheckState(GameState):
   def update(self, inputs):
      matches = self.grid.getMatches(3)
      if len(matches) > 0:
         return RemoveState(self.grid, matches)
      else:
         return SpawnState(self.grid)

#removes matches from the grid
   #Remove -> Fall
class RemoveState(GameState):
   def __init__(self, gridManager, matches):
      self.matches = matches
      self.grid = gridManager
   def update(self, inputs):
      self.grid.removeMatches(self.matches)
      return FallState(self.grid)

#moves block down
   #Fall -> Check
class FallState(GameState):
   def update(self, inputs):
      self.grid.moveCellsDown()
      return CheckState(self.grid)

#spawns new blocks into the grid
   #Spawn -> Fall (new blocks spawned)
   #      -> Ready (no new blocks spawned)
class SpawnState(GameState):
   def update(self, inputs):
      emptyCells = self.grid.getEmptyCells()
      if len(emptyCells) > 0:
         self.grid.spawnNewCells(emptyCells)
         return FallState(self.grid)
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
               return SpawnState(self.grid)
            #delete a block from the grid, causing other blocks to fall
            elif event.key == pygame.K_DELETE:
               self.grid.deleteBlock()
               return FallState(self.grid)
      return self


#state machine
class GameDirector:
   def __init__(self, gridManager):
      self.grid = gridManager
      self.currentState = ReadyState(self.grid)
   def update(self, inputs):
      self.currentState = self.currentState.update(inputs)
   def draw(self, screen):
      gridPos = ((1280/2 - 300),(720/2 - 300))
      screen.fill((200,200,200))
      self.grid.draw(screen, gridPos)

