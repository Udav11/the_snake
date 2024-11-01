from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня
ROCK_COLOR = (105, 105, 105)

# Цвет мусора
GARBAGE_COLOR = (160, 82, 45)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.

class GameObject:
    """класс GameObject"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Метод draw класса GameObject"""
        pass


class Rock(GameObject):
    """класс камня"""

    def __init__(self):
        super().__init__()
        self.body_color = ROCK_COLOR

    def randomize_position(self):
        """Spawn rock"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод draw класса Rock"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Garbage(GameObject):
    """класс мусора"""

    def __init__(self):
        super().__init__()
        self.body_color = GARBAGE_COLOR

    def randomize_position(self):
        """Spawn garbage"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод draw класса garbage"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """класс Apple"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Spawn apple"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Метод draw класса Apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """класс Snake"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """# Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод отвечающий за движение змейки."""
        head_x, head_y = self.get_head_position()

        head_x += self.direction[0] * GRID_SIZE
        head_y += self.direction[1] * GRID_SIZE

        if head_x < 0:
            head_x = SCREEN_WIDTH - GRID_SIZE
        elif head_x >= SCREEN_WIDTH:
            head_x = 0

        if head_y < 0:
            head_y = SCREEN_HEIGHT - GRID_SIZE
        elif head_y >= SCREEN_HEIGHT:
            head_y = 0
        self.last = self.positions[-1]
        self.positions.insert(0, (head_x, head_y))
        if self.length >= 1:
            if len(self.positions) > self.length:
                self.positions.pop(self.length)

    def draw(self):
        """Метод draw класса Snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        """Отрисовка головы змейки"""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            """Затирание последнего сегмента"""
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Get head pos"""
        return self.positions[0]

    def reset(self):
        """Метод для сброса положения змейки."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """управление клавишами"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
    return game_object.next_direction


def main():
    """Инициализация PyGame:"""
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    rock = Rock()
    garbage = Garbage()
    apple.randomize_position()
    rock.randomize_position()
    garbage.randomize_position()
    snake.move()
    snake.update_direction()
    SPEED = 10
    while True:
        snake.move()
        snake.update_direction()
        clock.tick(SPEED)
        handle_keys(snake)

        while snake.length < 3:
            SPEED = 10

        while snake.length > 3 and snake.length < 6:
            """Увеличиваем скорость"""
            SPEED = 15

        while snake.length >= 6:
            """увеличиваем до максимума"""
            SPEED = 20

        if snake.get_head_position() == apple.position or apple.position == snake.positions[1:]:
            """съедаем яблоко"""
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            """начинаем заново если ударились об себя"""
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position()
        if snake.get_head_position() == rock.position:
            """начинаем заново если ударились об камень"""
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            rock.randomize_position()
        if snake.get_head_position() == garbage.position:
            """съедаем мусор"""
            snake.length -= 1
            garbage.randomize_position()
            snake.positions.pop(snake.length)
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.length < 1:
            """начинаем заново если длина меньше 1"""
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            rock.randomize_position()
            apple.randomize_position()
            garbage.randomize_position()
        apple.draw()
        snake.draw()
        rock.draw()
        garbage.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
