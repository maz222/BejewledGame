from GridManager import ColorGrid
from BaseBlock import BaseBlock

from GameDirector import GameDirector

import pygame

grid = ColorGrid(7)
empty = grid.getEmptyCells()
print(grid)
pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
clock = pygame.time.Clock()

director = GameDirector(grid)

scoreFont = pygame.font.Font(None, 72)
scoreCount = 0
scoreLabel = scoreFont.render(str(scoreCount), True, (0,0,0))

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    director.update(events)
    director.draw(screen)
    screen.blit(scoreLabel, (1280/2-scoreLabel.get_width()/2,720/2-scoreLabel.get_height()/2+250))
    pygame.display.flip()
    clock.tick(60)
