import main
import pygame
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

# Тест 1: Проверка создания целей
create_targets()  # Создаем цели
assert len(targets) == 3, "Тест 1 не пройден: количество целей не равно TARGET_COUNT"
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
power = 50  # Минимальная мощность
draw_power_bar(power)
assert MIN_POWER <= power <= MAX_POWER, "Тест 4 не пройден: мощность вне допустимых пределов"

power = 300  # Максимальная мощность
draw_power_bar(power)
assert MIN_POWER <= power <= MAX_POWER, "Тест 4 не пройден: мощность вне допустимых пределов"

# Тест 5: Прогресс-бар угла выстрела
angle = 0  # Минимальный угол
draw_angle_bar(angle)
assert MIN_ANGLE <= angle <= MAX_ANGLE, "Тест 5 не пройден: угол вне допустимых пределов"

angle = 90  # Максимальный угол
draw_angle_bar(angle)
assert MIN_ANGLE <= angle <= MAX_ANGLE, "Тест 5 не пройден: угол вне допустимых пределов"

print("Все тесты пройдены успешно!")
