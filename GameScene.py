import pygame
from GridManager import ColorGrid
from BaseBlock import BaseBlock
from ScoreKeeper import ScoreKeeper

from GameDirector import GameDirector
#base gamescene boilerplate
class GameScene:
	def __init__(self, gameData=None):
		self.gameData = gameData
	def update(self, inputs=None):
		pass
	def draw(self, screen):
		pass

#instructions on how to play
class IntroScene(GameScene):
	def update(self,inputs=None):
		for event in inputs:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return PlayScene(self.gameData)
		return self
	def draw(self, screen):
		font = pygame.font.Font(None, 36)
		label1 = font.render("Arrow keys to move", True, (0,0,0))
		label2 = font.render("Delete to remove a block", True, (0,0,0))
		label3 = font.render("Enter to begin", True, (255,0,0))
		center = (1280/2,720/2)
		screen.fill((200,200,200))
		screen.blit(label1, (center[0]-label1.get_width()/2,center[1]-label2.get_height()-label1.get_height()/2 - 10))
		screen.blit(label2, (center[0]-label2.get_width()/2,center[1]-label2.get_height()/2))
		screen.blit(label3, (center[0]-label3.get_width()/2,center[1]-label2.get_height()+label3.get_height() + 20))

#the actual game!
class PlayScene(GameScene):
	def __init__(self, gameData=None):
		self.gameData = gameData
		self.director = GameDirector()
	def update(self, inputs=None):
		self.director.update(inputs)
		return self
	def draw(self, screen):
		self.director.draw(screen)

class SceneManager:
	def __init__(self, startingScene=None):
		self.currentScene = IntroScene()
	def update(self, inputs=None):
		self.currentScene = self.currentScene.update(inputs)
	def draw(self, screen):
		self.currentScene.draw(screen)
