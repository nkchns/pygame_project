import pygame, random

pygame.init()
size = width, height = 700, 500
screen = pygame.display.set_mode(size)
window_icon = pygame.image.load('icons/icon.png')
pygame.display.set_icon(window_icon)
pygame.display.set_caption('Snake')


fps = 20
clock = pygame.time.Clock()
running = True

defeat = False  # Переменная поражения
score = 1  # Счет игрока

snake_pos = [30, 10]  # Координаты головы змейки
snake_list = [[30, 10]]  # Список с координатами всех сегментов змейки
snake_direction = 'right'  # Направление, куда движется змейка

food_pos = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]  # Координаты обычной еды, выбираются случайно
extra_food = [random.randrange(10, 700, 10),
              random.randrange(10, 500, 10)]  # Координаты редкой еды, выбираются случайно


# Механика движения змейки
def movement_mechanic(direction):
    if direction == 'up':
        snake_pos[1] -= 10
    elif direction == 'down':
        snake_pos[1] += 10
    elif direction == 'right':
        snake_pos[0] += 10
    elif direction == 'left':
        snake_pos[0] -= 10


# Механика поражения
def defeat_mechanic(pos):
    global defeat
    # Если змейка выходит за границы X окна
    if pos[0] < 0 or pos[0] >= width:
        defeat = True  # Начисляется поражение
        print('defeated by width')
    # Если змейка выходит за границы Y окна
    if pos[1] < 0 or pos[1] >= height:
        defeat = True  # Начисляется поражение
        print('defeated by height')
    # Если змейка сталкивается сама с собой
    for segment in snake_list:
        if segment == pos:
            defeat = True  # Начисляется поражение
            print('defeated by yourself')


# Обычная еда, увеличивает счет на 1
def basic_eating_mechanic(snake_position, food_position):
    global score, food_pos

    snake_list.insert(0, list(snake_pos))  # В список змейки на место головы вставляется новый элемент
    if snake_position == food_position:
        # Если змейка касается еды, то счет увеличивается, а новой еде присваиются другие случайные координаты
        score += 1
        food_pos = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]
        print(score)
    else:
        # Если змейка не касается еды, то последний элемент удаляется
        snake_list.pop()


# Редкая еда, увеличивает счет на 5 и появляется раз в 10 ходов
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


# Основной цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Управление змейкой стрелочками
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

    screen.fill(pygame.Color(0, 0, 0))

    movement_mechanic(snake_direction)
    defeat_mechanic(snake_pos)

    if score % 10 != 0 or score == 0:
        # Если счет не кратен 10, то еда обычная и змейка белого цвета
        [pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(i[0], i[1], 10, 10)) for i in
         snake_list]  # Списочное выражение рисует белую змейку
        pygame.draw.rect(screen, pygame.Color(255, 255, 255),
                         pygame.Rect(food_pos[0], food_pos[1], 10, 10))  # Рисуется обычная еда

        basic_eating_mechanic(snake_pos, food_pos)
    elif score % 10 == 0:
        # Если счет кратен 10, то еда редкая (зеленая) и змейка зеленого цвета
        [pygame.draw.rect(screen, pygame.Color(0, 255, 0), pygame.Rect(i[0], i[1], 10, 10)) for i in
         snake_list]  # Списочное выражение рисует зеленую змейку
        pygame.draw.rect(screen, pygame.Color(0, 255, 0),
                         pygame.Rect(extra_food[0], extra_food[1], 10, 10))  # Рисуется редкая еда

        extra_eating_mechanic(snake_pos, extra_food)

    # Проверяется наличие поражения, если да, то игра сразу начинается заново
    if defeat:
        defeat = False
        score = 1
        snake_pos = [30, 10]
        snake_list = [[30, 10]]
        snake_direction = 'right'
        food_pos = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]
        extra_food = [random.randrange(10, 700, 10), random.randrange(10, 500, 10)]

    pygame.display.flip()
    clock.tick(fps)
