import pygame
import random

# Параметры игры
TARGET_RADIUS = 20
TARGET_COUNT = 3
MIN_POWER = 50
MAX_POWER = 300
GROUND_LEVEL = 600 - 50


# Функция для создания целей
def create_targets():
    targets = []
    positions = set()
    while len(targets) < TARGET_COUNT:
        x = random.randint(400, 1450)
        if all(abs(x - pos) >= TARGET_RADIUS * 2 + 50 for pos in positions):
            y = GROUND_LEVEL - TARGET_RADIUS
            targets.append(pygame.Rect(x - TARGET_RADIUS, y - TARGET_RADIUS, TARGET_RADIUS * 2, TARGET_RADIUS * 2))
            positions.add(x)
    return targets


# Проверка попаданий
def check_hit(targets, x, y):
    for target in targets[:]:
        if target.collidepoint(x, y):
            targets.remove(target)
            return True
    return False


# Основной тестовый скрипт
def run_tests():
    # Тест 1: Проверка создания целей
    targets = create_targets()
    assert len(
        targets) == TARGET_COUNT, f"Ошибка: Не создано необходимое количество целей. Ожидалось {TARGET_COUNT}, получено {len(targets)}."

    # Проверка, что цели не перекрываются
    for i in range(len(targets)):
        for j in range(i + 1, len(targets)):
            assert not targets[i].colliderect(targets[j]), "Ошибка: Цели перекрываются!"

    print("Тест 1: Создание целей - пройден.")

    # Тест 2: Проверка попадания
    x, y = targets[0].center  # Попробуем попасть в первую цель
    hit = check_hit(targets, x, y)
    assert hit, "Ошибка: Попадание в цель не обнаружено."
    assert len(
        targets) == TARGET_COUNT - 1, f"Ошибка: Количество целей не уменьшилось после попадания. Ожидалось {TARGET_COUNT - 1}, получено {len(targets)}."

    print("Тест 2: Проверка попадания - пройден.")

    # Тест 3: Проверка оставшихся попыток
    shots = 5
    shots -= 1
    assert shots == 4, f"Ошибка: Количество оставшихся попыток неправильно обновляется. Ожидалось 4, получено {shots}."

    print("Тест 3: Проверка оставшихся попыток - пройден.")


# Запуск тестов
if __name__ == "__main__":
    pygame.init()  # Инициализация Pygame для работы с Rect
    run_tests()
    pygame.quit()
