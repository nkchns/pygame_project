import pygame, random

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)

fps = 50
clock = pygame.time.Clock()
running = True


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color(0, 0, 0))
    pygame.display.flip()
    clock.tick(fps)
