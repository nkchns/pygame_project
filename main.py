import pygame, random

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)

fps = 20
clock = pygame.time.Clock()
running = True

defeat = False
score = 1

snake_pos = [30, 10]
snake_list = [[30, 10]]
snake_direction = 'right'

food_pos = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]
extra_food = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]

def movement_mechanic(direction):
    if direction == 'up':
        snake_pos[1] -= 10
    elif direction == 'down':
        snake_pos[1] += 10
    elif direction == 'right':
        snake_pos[0] += 10
    elif direction == 'left':
        snake_pos[0] -= 10

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if snake_direction == 'right' or snake_direction == 'left':
                    snake_direction = 'up'
            if event.key == pygame.K_DOWN:
                if snake_direction == 'right' or snake_direction == 'left':
                    snake_direction = 'down'
            if event.key == pygame.K_RIGHT:
                if snake_direction == 'up' or snake_direction == 'down':
                    snake_direction = 'right'
            if event.key == pygame.K_LEFT:
                if snake_direction == 'up' or snake_direction == 'down':
                    snake_direction = 'left'

    movement_mechanic(snake_direction)

    screen.fill(pygame.Color(0, 0, 0))
    [pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(i[0], i[1], 10, 10)) for i in snake_list]

    snake_list.insert(0, list(snake_pos))
    snake_list.pop()
    pygame.display.flip()
    clock.tick(fps)
