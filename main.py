import pygame
import random
import os
import sys

pygame.init()
size = width, height = 720, 512
screen = pygame.display.set_mode(size)
window_icon = pygame.image.load('icons/icon.png')  # Иконка окна
pygame.display.set_icon(window_icon)
pygame.display.set_caption('Snake')  # Заголовок окна

fps = 25
clock = pygame.time.Clock()
running = True

defeat = False  # Переменная поражения
score = 1  # Счет игрока

snake_pos = [32, 16]  # Координаты головы змейки
snake_list = [[32, 16]]  # Список с координатами всех сегментов змейки
snake_direction = 'right'  # Направление, куда движется змейка

basic_food = [random.randrange(16, 720, 16),
              random.randrange(16, 512, 16)]  # Координаты обычной еды, выбираются случайно
extra_food = [random.randrange(16, 720, 16),
              random.randrange(16, 512, 16)]  # Координаты редкой еды, выбираются случайно


def terminate():
    pygame.quit()
    sys.exit()


# Функция для загрузки спрайтов
def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    image = pygame.image.load(fullname)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


apple_sprite = pygame.sprite.Group()  # Спрайт обычной еды
apple = pygame.sprite.Sprite()
apple.image = load_image("icons/apple.png")
apple.rect = apple.image.get_rect()
apple_sprite.add(apple)
apple.rect.x = basic_food[0]
apple.rect.y = basic_food[1]

cherry_sprite = pygame.sprite.Group()  # Спрайт редкой еды
cherry = pygame.sprite.Sprite()
cherry.image = load_image("icons/cherries.png")
cherry.rect = cherry.image.get_rect()
cherry_sprite.add(cherry)
cherry.rect.x = extra_food[0]
cherry.rect.y = extra_food[1]


# Механика движения змейки
def movement_mechanic(direction):
    if direction == 'up':
        snake_pos[1] -= 16
    elif direction == 'down':
        snake_pos[1] += 16
    elif direction == 'right':
        snake_pos[0] += 16
    elif direction == 'left':
        snake_pos[0] -= 16


# Механика поражения
def defeat_mechanic(pos):
    global defeat
    # Если змейка выходит за границы X окна
    if pos[0] < 0 or pos[0] >= width:
        defeat = True  # Начисляется поражение
        print('out of borders')
    # Если змейка выходит за границы Y окна
    if pos[1] < 0 or pos[1] >= height:
        defeat = True  # Начисляется поражение
        print('out of borders')
    # Если змейка сталкивается сама с собой
    for segment in snake_list:
        if segment == pos:
            defeat = True  # Начисляется поражение
            print('defeated by yourself')


# Обычная еда, увеличивает счет на 1
def basic_eating_mechanic(snake_position, food_position):
    global score, basic_food

    snake_list.insert(0, list(snake_pos))  # В список змейки на место головы вставляется новый элемент
    if snake_position == food_position:
        # Если змейка касается еды, то счет увеличивается, а новой еде присваиются другие случайные координаты
        score += 1
        basic_food = [random.randrange(16, 720, 16), random.randrange(16, 512, 16)]
        apple.rect.x = basic_food[0]
        apple.rect.y = basic_food[1]
        print('Счет:', score)
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
        extra_food = [random.randrange(16, 720, 16), random.randrange(16, 512, 16)]
        cherry.rect.x = extra_food[0]
        cherry.rect.y = extra_food[1]
        print('Счет:', score)
    else:
        snake_list.pop()


# Заставка
def start_screen():
    intro_text = ["Snake game", "", "",
                  "Для началы игры", "нажмите любую кнопку", "",
                  "Для управления", "используйте стрелочки", "", "Для выхода", "нажмите ESC"]

    fon = pygame.transform.scale(load_image('icons/fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 45)
    text_coord = 30
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('White'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 150
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        pygame.display.flip()
        clock.tick(fps)


start_screen()

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
            if event.key == pygame.K_ESCAPE:
                terminate()

    screen.fill(pygame.Color(0, 0, 0))
    font = pygame.font.Font(None, 35)
    text = font.render('Счет: ' + str(score), 1, (150, 150, 150))
    screen.blit(text, (10, 10))

    movement_mechanic(snake_direction)
    defeat_mechanic(snake_pos)

    if score % 10 != 0 or score == 0:
        # Если счет не кратен 10, то еда обычная и змейка белого цвета
        [pygame.draw.rect(screen, pygame.Color(255, 255, 255), pygame.Rect(i[0], i[1], 16, 16)) for i in
         snake_list]  # Списочное выражение рисует белую змейку
        pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                         pygame.Rect(basic_food[0], basic_food[1], 16, 16))  # Рисуется обычная еда
        apple_sprite.draw(screen)

        basic_eating_mechanic(snake_pos, basic_food)
    elif score % 10 == 0:
        # Если счет кратен 10, то еда редкая (зеленая) и змейка зеленого цвета
        [pygame.draw.rect(screen, pygame.Color(0, 255, 0), pygame.Rect(i[0], i[1], 16, 16)) for i in
         snake_list]  # Списочное выражение рисует зеленую змейку
        pygame.draw.rect(screen, pygame.Color(0, 0, 0),
                         pygame.Rect(extra_food[0], extra_food[1], 16, 16))  # Рисуется редкая еда
        cherry_sprite.draw(screen)

        extra_eating_mechanic(snake_pos, extra_food)

    # Проверяется наличие поражения, если да, то игра сразу начинается заново
    if defeat:
        defeat = False
        score = 1
        snake_pos = [32, 16]
        snake_list = [[32, 16]]
        snake_direction = 'right'
        basic_food = [random.randrange(16, 720, 16), random.randrange(16, 512, 16)]
        extra_food = [random.randrange(16, 720, 16), random.randrange(16, 512, 16)]

        apple.rect.x = basic_food[0]
        apple.rect.y = basic_food[1]
        cherry.rect.x = extra_food[0]
        cherry.rect.y = extra_food[1]

    pygame.display.flip()
    clock.tick(fps)
