import pygame
from SimpleVector import SimplePoly


pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
clock = pygame.time.Clock()

testPoly = SimplePoly([(100,100),(200,100),(200,200),(100,200)])

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    testPoly.rotateSelf(10)
    testPoly.scaleInPlace(-.1)
    screen.fill((255,255,255))
    pygame.draw.polygon(screen, (255,0,0), testPoly.getPoints())
    pygame.display.flip()
    clock.tick(60)