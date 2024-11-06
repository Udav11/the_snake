from random import randint, choice

import pygame as pg

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

# Центр поля
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """класс GameObject"""

    def __init__(self, position=SCREEN_CENTER, color=None):
        self.position = position
        self.body_color = color

    def draw(self):
        """Метод draw класса GameObject"""
        raise NotImplementedError('Метод должен быть определен'
                                  'в дочерних классах')


class StaticObject(GameObject):
    """Класс для статичных объектов"""

    def __init__(self, position=SCREEN_CENTER, color=None, occupied=[]):
        super().__init__(position, color)
        self.randomize_position(occupied)

    def draw(self):
        """Метод draw класса Apple"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied=[]):
        """Случайный спавн объекта"""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied:
                break


class Rock(StaticObject):
    """Класс камня"""

    def __init__(self, position=SCREEN_CENTER, color=ROCK_COLOR, occupied=[]):
        super().__init__(position, color)


class Garbage(StaticObject):
    """Класс плохой еды"""

    def __init__(self, position=SCREEN_CENTER, color=GARBAGE_COLOR,
                 occupied=[]):
        super().__init__(position, color)


class Apple(StaticObject):
    """класс Apple"""

    def __init__(self, position=SCREEN_CENTER, color=APPLE_COLOR, occupied=[]):
        super().__init__(position, color)


class Snake(GameObject):
    """класс Snake"""

    def __init__(self, position=SCREEN_CENTER, color=SNAKE_COLOR, last=None):
        super().__init__(position, color)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод отвечающий за движение змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        head_x = (head_x + (dir_x * GRID_SIZE)) % SCREEN_WIDTH
        head_y = (head_y + (dir_y * GRID_SIZE)) % SCREEN_HEIGHT

        self.positions.insert(0, (head_x, head_y))
        self.last = (
            self.positions.pop() if self.length < len(self.positions)
            else None
        )

    def draw(self):
        """Отрисовка головы змейки"""
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            """Затирание последнего сегмента"""
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получаем координаты головы змеи"""
        return self.positions[0]

    def reset(self):
        """Метод для сброса положения змейки."""
        self.length = 1
        self.last = None
        self.positions = [self.position]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None


def handle_keys(game_object):
    """Управление клавишами"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def update_positions(snake, static_objects):
    """Обновление координат статичных объектов"""
    occupied = [*snake.positions]
    for static_object in static_objects:
        static_object.randomize_position(occupied)
        occupied.append(static_object.position)


def main():
    """Инициализация pg:"""
    pg.init()
    # Тут нужно создать экземпляры классов.
    occupied = []
    snake = Snake()
    occupied.append(snake.positions)
    apple = Apple(occupied)
    occupied.append(apple.position)
    rock = Rock(occupied)
    occupied.append(rock.position)
    garbage = Garbage(occupied)
    occupied.append(garbage.position)

    while True:
        snake.move()
        snake.update_direction()
        clock.tick(SPEED)
        handle_keys(snake)
        occupied = [apple.position, garbage.position,
                    rock.position, *snake.positions]
        if (snake.get_head_position() == apple.position):
            """съедаем яблоко"""
            snake.length += 1
            apple.randomize_position(occupied)
        elif snake.get_head_position() in snake.positions[1:]:
            """начинаем заново если ударились об себя"""
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        elif snake.get_head_position() == rock.position:
            """начинаем заново если ударились об камень"""
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            update_positions(snake, [apple, rock, garbage])
        elif snake.get_head_position() == garbage.position:
            """съедаем мусор"""
            snake.length -= 1
            garbage.randomize_position(occupied)
            snake.positions.pop(snake.length)
            screen.fill(BOARD_BACKGROUND_COLOR)

        if snake.length < 1:
            """начинаем заново если длина меньше 1"""
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            update_positions(snake, [apple, rock, garbage])

        apple.draw()
        snake.draw()
        rock.draw()
        garbage.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
