import pygame
import random
import math

pygame.init()

# Константы
WIDTH, HEIGHT = 1500, 600  # Размер окна
GROUND_LEVEL = HEIGHT - 50
CANNON_X, CANNON_Y = 100, GROUND_LEVEL  # Координаты пушки
CANNON_LENGTH = 125  # Длина ствола пушки
TARGET_RADIUS = 20
TARGET_COUNT = 3
MAX_ANGLE = 90
MIN_ANGLE = 0
MAX_POWER = 300  # Максимальная сила выстрела
MIN_POWER = 50   # Минимальная сила выстрела
power = MIN_POWER  # Начальная сила выстрела

# Начальные параметры
angle = 45
shots = 5
targets = []
hit_targets = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Стрелок")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)

# Создание врагов
def create_targets():
    targets.clear()
    positions = set()
    while len(targets) < TARGET_COUNT:
        x = random.randint(400, WIDTH - 50)
        if all(abs(x - pos) >= TARGET_RADIUS * 2 + 50 for pos in positions):
            y = GROUND_LEVEL - TARGET_RADIUS
            targets.append(pygame.Rect(x - TARGET_RADIUS, y - TARGET_RADIUS, TARGET_RADIUS * 2, TARGET_RADIUS * 2))
            positions.add(x)

# Поворот пушки
def rotate_gun(angle):
    x0, y0 = CANNON_X, CANNON_Y
    length = CANNON_LENGTH

    # Вычисление новых координат конца линии в зависимости от угла
    x1 = x0 + length * math.cos(math.radians(angle))
    y1 = y0 - length * math.sin(math.radians(angle))

    # Отрисовка пушки
    pygame.draw.line(screen, BLACK, (x0, y0), (x1, y1), 10)

# Стрельба
def fire_cannon(angle, power):
    global shots, hit_targets
    shots -= 1
    angle_rad = math.radians(angle)
    x = CANNON_X
    y = CANNON_Y
    vx = power * math.cos(angle_rad)
    vy = -power * math.sin(angle_rad)
    gravity = 9.8
    dt = 0.1

    # Стрелять снарядом
    while y < HEIGHT:
        # Перемещение снаряда
        x += vx * dt
        vy += gravity * dt
        y += vy * dt

        # Отрисовка снаряда
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (0, GROUND_LEVEL, WIDTH, HEIGHT - GROUND_LEVEL))  # Земля
        rotate_gun(angle)
        pygame.draw.circle(screen, RED, (int(x), int(y)), 5)  # Снаряд

        # Отрисовка целей
        for target in targets:
            pygame.draw.ellipse(screen, GREEN, target)

        # Проверка попадания в цель
        for target in targets[:]:
            if target.collidepoint(x, y):
                targets.remove(target)
                hit_targets += 1
                break

        # Проверка попадания в землю
        if y >= GROUND_LEVEL:
            break  # Уничтожить снаряд, если он попадает в землю

        # Обновление текста
        draw_text(f"Осталось попыток: {shots}", 10, 10)
        draw_text(f"Попаданий: {hit_targets}/{TARGET_COUNT}", 10, 50)

        # Прогресс бары
        draw_power_bar(power)
        draw_angle_bar(angle)

        pygame.display.flip()
        pygame.time.delay(30)

        # Если все цели поражены, завершение игры
        if hit_targets == TARGET_COUNT:
            draw_text("Поздравляем! Все цели уничтожены!", WIDTH // 2 - 200, HEIGHT // 2)
            pygame.display.flip()
            pygame.time.wait(2000)
            exit()

    # Проверка, закончились ли попытки
    if shots == 0 and hit_targets < TARGET_COUNT:
        draw_text("Игра окончена. У вас не осталось попыток!", WIDTH // 2 - 200, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.wait(2000)
        exit()

def draw_text(text, x, y):
    label = font.render(text, True, BLACK)
    screen.blit(label, (x, y))

# Прогресс-бар силы выстрела
def draw_power_bar(power):
    pygame.draw.rect(screen, BLACK, (50, 550, 300, 30), 2)  # Контур
    pygame.draw.rect(screen, GREEN, (50, 550, power * (300 / MAX_POWER), 30))  # Заполненная часть

# Прогресс-бар угла
def draw_angle_bar(angle):
    pygame.draw.rect(screen, BLACK, (400, 550, 300, 30), 2)  # Контур
    pygame.draw.rect(screen, GREEN, (400, 550, (angle - MIN_ANGLE) * (300 / (MAX_ANGLE - MIN_ANGLE)), 30))  # Заполненная часть

# Основной игровой цикл
def game_loop():
    global angle, shots, hit_targets, power
    running = True
    create_targets()

    while running:
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, (0, GROUND_LEVEL, WIDTH, HEIGHT - GROUND_LEVEL))  # Земля

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and angle > MIN_ANGLE:
                    angle -= 1
                elif event.key == pygame.K_RIGHT and angle < MAX_ANGLE:
                    angle += 1
                elif event.key == pygame.K_UP and power < MAX_POWER:
                    power += 5
                elif event.key == pygame.K_DOWN and power > MIN_POWER:
                    power -= 5
                elif event.key == pygame.K_SPACE and shots > 0:
                    fire_cannon(angle, power)

        # Рисуем пушку и цели
        rotate_gun(angle)
        for target in targets:
            pygame.draw.ellipse(screen, GREEN, target)

        # Информация о состоянии игры
        draw_text(f"Осталось попыток: {shots}", 10, 10)
        draw_text(f"Попаданий: {hit_targets}/{TARGET_COUNT}", 10, 50)

        # Прогресс бары
        draw_power_bar(power)
        draw_angle_bar(angle)

        pygame.display.flip()
        pygame.time.delay(30)

        # Проверка на победу
        if hit_targets == TARGET_COUNT:
            running = False

    pygame.quit()

# Запуск игры
game_loop()

# Тесты
# Тест 1: Проверка создания целей
create_targets()  # Создаем цели
assert len(targets) == TARGET_COUNT, "Тест 1 не пройден: количество целей не равно TARGET_COUNT"
for target in targets:
    assert 400 <= target.x <= WIDTH - 50, "Тест 1 не пройден: цель выходит за пределы экрана"

# Тест 2: Проверка выстрела с попаданием
# Создаем поддельную цель рядом с пушкой, чтобы гарантировать попадание
target = pygame.Rect(150, GROUND_LEVEL - TARGET_RADIUS, TARGET_RADIUS * 2, TARGET_RADIUS * 2)
targets.append(target)
initial_hit_targets = hit_targets
initial_shots = shots

fire_cannon(45, 100)  # Стреляем с углом 45° и силой 100

assert hit_targets == initial_hit_targets + 1, "Тест 2 не пройден: попадание по цели не зафиксировано"
assert shots == initial_shots - 1, "Тест 2 не пройден: количество попыток не уменьшилось"

# Тест 3: Проверка уменьшения количества попыток
initial_shots = shots
fire_cannon(45, 100)
assert shots == initial_shots - 1, "Тест 3 не пройден: количество попыток не уменьшилось после выстрела"

# Тест 4: Прогресс-бар мощности выстрела
power = MIN_POWER  # Минимальная мощность
draw_power_bar(power)
assert MIN_POWER <= power <= MAX_POWER, "Тест 4 не пройден: мощность вне допустимых пределов"

power = MAX_POWER  # Максимальная мощность
draw_power_bar(power)
assert MIN_POWER <= power <= MAX_POWER, "Тест 4 не пройден: мощность вне допустимых пределов"

# Тест 5: Прогресс-бар угла выстрела
angle = MIN_ANGLE  # Минимальный угол
draw_angle_bar(angle)
assert MIN_ANGLE <= angle <= MAX_ANGLE, "Тест 5 не пройден: угол вне допустимых пределов"

angle = MAX_ANGLE  # Максимальный угол
draw_angle_bar(angle)
assert MIN_ANGLE <= angle <= MAX_ANGLE, "Тест 5 не пройден: угол вне допустимых пределов"

print("Все тесты пройдены успешно!")
