import pygame
import random

# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 600

# Цвета
WHITE = (255, 255, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Летающий корабль")

# Загрузка изображений
bg_image = pygame.image.load("bg.png")
ship_image = pygame.image.load("ship.png")
obstacle_image = pygame.image.load("obstacle.png")

# Размеры корабля и препятствия
SHIP_WIDTH = 50
SHIP_HEIGHT = 30
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 200

# Позиция корабля
ship_x = 100
ship_y = HEIGHT // 2 - SHIP_HEIGHT // 2

# Скорость корабля
ship_speed = 5

# Создание списка препятствий
obstacles = []

# Время для управления частотой появления препятствий
obstacle_spawn_time = 0

# Счет игры
score = 0

# Шрифт для отображения счёта
font = pygame.font.Font(None, 36)

# Главный игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление кораблём
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ship_y -= ship_speed
    if keys[pygame.K_DOWN]:
        ship_y += ship_speed

    # Обновление позиции препятствий
    for obstacle in obstacles:
        obstacle[0] -= ship_speed

    # Создание нового препятствия
    obstacle_spawn_time += clock.get_rawtime()
    if obstacle_spawn_time >= 400:
        obstacle_spawn_time = 0
        obstacle_y = random.randint(0, HEIGHT - OBSTACLE_HEIGHT)
        obstacles.append([WIDTH, obstacle_y])

    # Удаление препятствий за пределами экрана
    for obstacle in obstacles:
        if obstacle[0] + OBSTACLE_WIDTH < 0:
            obstacles.remove(obstacle)
            score += 1
    
    # Проверка столкновения с препятствиями
    for obstacle in obstacles:
        if (ship_x + SHIP_WIDTH > obstacle[0] and ship_x < obstacle[0] + OBSTACLE_WIDTH) and \
                (ship_y + SHIP_HEIGHT > obstacle[1] and ship_y < obstacle[1] + OBSTACLE_HEIGHT):
            running = False

    # Отрисовка фона
    screen.blit(bg_image, (0, 0))

    # Отрисовка корабля
    screen.blit(ship_image, (ship_x, ship_y))

    # Отрисовка препятствий
    for obstacle in obstacles:
        screen.blit(obstacle_image, (obstacle[0], obstacle[1]))

    # Отрисовка счета
    score_text = font.render("Счёт: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

# Экран проигрыша
game_over_font = pygame.font.Font(None, 72)
game_over_text = game_over_font.render("Игра окончена", True, (0, 0, 0))
screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
pygame.display.flip()
pygame.time.wait(5000)  # Подождать 5 секунд перед закрытием

pygame.quit()
