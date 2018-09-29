from BaseBlock import BaseBlock
from BlockArmor import BlockArmor

from GridCell import GridCellContainer

from BlockFactory import BlockFactory

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
center = (1280/2 - 25, 720/2 - 25)
done = False
clock = pygame.time.Clock()

factory = BlockFactory()

cell = factory.build(center)

scale = 0

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DELETE:
                cell = factory.build(center)
    if scale >= 1:
        scale = 0
    scale += .05
    #update blocks
    #cell.rotateAroundPoint(5,center)
    #cell.rotateInPlace(5)
    cell.scale(1+scale)
    screen.fill((200,200,200))
    #Draw blocks
    cell.draw(screen)
    pygame.display.flip()
    clock.tick(60)