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


def basic_eating_mechanic(snake_position, food_position):
    global score, food_pos

    snake_list.insert(0, list(snake_pos))
    if snake_position == food_position:
        score += 1
        food_pos = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]
        print(score)
    else:
        snake_list.pop()


def extra_eating_mechanic(snake_position, extra_food_position):
    global score, extra_food

    snake_list.insert(0, list(snake_pos))
    if snake_position == extra_food_position:
        for i in range(4):
            snake_list.insert(0, list(snake_pos))
        score += 5
        extra_food = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]
        print(score)
    else:
        snake_list.pop()


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

    if score % 10 != 0 or score == 0:
        [pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(i[0], i[1], 10, 10)) for i in snake_list]
        pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        basic_eating_mechanic(snake_pos, food_pos)
    elif score % 10 == 0:
        [pygame.draw.rect(screen, pygame.Color(0, 255, 0), pygame.Rect(i[0], i[1], 10, 10)) for i in snake_list]
        pygame.draw.rect(screen, pygame.Color(0, 255, 0), pygame.Rect(extra_food[0], extra_food[1], 10, 10))
        extra_eating_mechanic(snake_pos, extra_food)

    pygame.display.flip()
    clock.tick(fps)
