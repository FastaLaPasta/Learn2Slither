from settings import TILE_SIZE, COLS, ROWS
import pygame as pg
from random import choice


class Apple:
    def __init__(self, snake):
        self.pos = pg.Vector2(5, 8)
        self.screen = pg.display.get_surface()
        self.snake = snake
        self.set_pos()

    def set_pos(self):
        available_pos = [pg.Vector2(x, y) for x in range(COLS)
                         for y in range(ROWS)
                         if pg.Vector2(x, y) not in self.snake.body]
        self.pos = choice(available_pos)

    def draw(self):
        rect = pg.Rect(self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE,
                       TILE_SIZE, TILE_SIZE)
        pg.draw.rect(self.screen, 'blue', rect)
