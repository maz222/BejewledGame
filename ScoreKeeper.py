import pygame

class ScoreKeeper:
	def __init__(self, position=(0,0), count=0):
		self.score = count
		self.position = position
	def addScore(self, value):
		self.score += value
	def setScore(self, value):
		self.score = value
	def getScore(self):
		return self.score
	def draw(self, screen, offset=(0,0)):
		scoreFont = pygame.font.Font(None, 72)
		scoreLabel = scoreFont.render(str(self.score), True, (0,0,0))
		screen.blit(scoreLabel, (1280/2-scoreLabel.get_width()/2,720/2-scoreLabel.get_height()/2+250))
