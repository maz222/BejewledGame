from GameScene import SceneManager

import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
done = False
clock = pygame.time.Clock()

manager = SceneManager()

while not done:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    manager.update(events)
    manager.draw(screen)
    pygame.display.flip()
    clock.tick(60)
