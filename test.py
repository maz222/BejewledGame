from GridManager import ColorGrid
from BaseBlock import BaseBlock

from GameDirector import GameDirector

import pygame

grid = ColorGrid(10)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
clock = pygame.time.Clock()

director = GameDirector(grid)

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    director.update(events)
    director.draw(screen)
    pygame.display.flip()
    clock.tick(60)
