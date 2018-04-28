from GridManager import ColorGrid
from BaseBlock import BaseBlock

from GameDirector import GameDirector

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
clock = pygame.time.Clock()

block = BaseBlock(1,(0,0))
block2 = BaseBlock(2,(60,0))
block3 = BaseBlock(3,(120,0))
center = (1280/2,720/2)

while not done:
	events = pygame.event.get()
	block.poly.rotateAroundPoint((85,25),1)
	block2.poly.rotateAroundPoint((85,25),1)
	block3.poly.rotateAroundPoint((85,25),1)

	for event in events:
		if event.type == pygame.QUIT:
			done=True
	screen.fill((200,200,200))
	block.draw(screen, center)
	block2.draw(screen, center)
	block3.draw(screen,center)
	pygame.display.flip()
	clock.tick(60)
