from settings import TILE_SIZE, COLS, ROWS
import pygame as pg
from random import choice


class GreenApple:
    def __init__(self, snake):
        self.pos = pg.Vector2(5, 8)
        self.screen = pg.display.get_surface()
        self.snake = snake
        self.occupied = []
        self.set_pos()

    def get_occupied_tile(self, occupied):
        self.occupied = occupied

    def set_pos(self):
        apple_pos = []
        if self.occupied:
            for apple in self.occupied:
                apple_pos.append(apple.pos)
        available_pos = [pg.Vector2(x, y) for x in range(COLS)
                         for y in range(ROWS)
                         if pg.Vector2(x, y) not in self.snake.body and
                         pg.Vector2(x, y) not in apple_pos]
        self.pos = choice(available_pos)

    def draw(self):
        rect = pg.Rect(self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE,
                       TILE_SIZE, TILE_SIZE)
        pg.draw.rect(self.screen, 'green', rect)


class RedApple:
    def __init__(self, snake, greenApples):
        self.pos = pg.Vector2(5, 8)
        self.screen = pg.display.get_surface()
        self.snake = snake
        self.greenApple = greenApples
        self.set_pos()

    def set_pos(self):
        apple_pos = [apple.pos for apple in self.greenApple]
        available_pos = [pg.Vector2(x, y) for x in range(COLS)
                         for y in range(ROWS)
                         if pg.Vector2(x, y) not in self.snake.body and
                         pg.Vector2(x, y) not in apple_pos]
        self.pos = choice(available_pos)

    def draw(self):
        rect = pg.Rect(self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE,
                       TILE_SIZE, TILE_SIZE)
        pg.draw.rect(self.screen, 'red', rect)
