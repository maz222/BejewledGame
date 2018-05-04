from GridManager import ColorGrid
from BaseBlock import BaseBlock
from ScoreKeeper import ScoreKeeper

from GameDirector import GameDirector

import pygame

grid = ColorGrid(7)
empty = grid.getEmptyCells()
print(grid)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
clock = pygame.time.Clock()

score = ScoreKeeper()
gameData = {}
gameData["grid"] = grid
gameData["score"] = score
director = GameDirector(gameData)


while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    director.update(events)
    director.draw(screen)
    pygame.display.flip()
    clock.tick(60)
