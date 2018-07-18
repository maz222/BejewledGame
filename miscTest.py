from GridManager import ColorGrid
from BaseBlock import BaseBlock

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
center = (1280/2 - 25, 720/2 - 25)
done = False
clock = pygame.time.Clock()

block1 = BaseBlock(2,(0,0))
block2 = BaseBlock(2,(60,0))
block3 = BaseBlock(2,(120,0))
block4 = BaseBlock(3,(0,60))
block5 = BaseBlock(3,(60,60))
block6 = BaseBlock(3,(120,60))
block7 = BaseBlock(4,(0,120))
block8 = BaseBlock(4,(60,120))
block9 = BaseBlock(4,(120,120))
blocks = [block1, block2, block3, block4, block5, block6, block7, block8, block9]

loop = False
count = 0

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            #check for rotations
            if event.key == pygame.K_LEFT and loop == False:
                #for b in blocks:
                #    print((int(b.getPosition()[0]), int(b.getPosition()[1])))
                #print("---") 
                loop = True
                count = 0
    if loop == True:
        n = 3
        #print(count)
        for b in blocks:
            #b.poly.rotateTo(count)
            b.rotateAroundPoint(2,(n*60/2-5, n*60/2-5))
            #b.poly.rotateBy(5)
        count += 2
        if count >= 90:
            loop = False
            #for b in blocks:
            #    print((int(b.getPosition()[0]), int(b.getPosition()[1])))
            #print("***")

    screen.fill((200,200,200))
    for b in blocks:
        b.draw(screen,(center[0]-60, center[1]-60))
    pygame.draw.rect(screen, (0,0,0), (center[0] - 60 - 5, center[1] - 5 - 60, 60, 60), 2)
    pygame.draw.rect(screen, (0,0,0), (center[0] + 60 - 5, center[1] - 5 + 60, 60, 60), 2)
    pygame.draw.rect(screen, (0,0,0), (center[0] - 75, center[1] - 75, 200, 200), 4)
    pygame.display.flip()
    clock.tick(60)