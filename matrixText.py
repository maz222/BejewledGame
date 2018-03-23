import pygame
from SimpleVector import BlockPoly





pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
#done = True
clock = pygame.time.Clock()

testPoly = BlockPoly((100,100),60,60)
scale = 1

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    testPoly.rotateBy(5)
    #testPoly.scaleTo(.99)
    screen.fill((255,255,255))
    pygame.draw.polygon(screen, (255,0,0), testPoly.getPoints())
    pygame.display.flip()
    clock.tick(60)