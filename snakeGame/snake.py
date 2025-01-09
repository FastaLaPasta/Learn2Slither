from settings import START_LENGTH, START_COL, START_ROW, TILE_SIZE
import pygame as pg


class Snake:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.body = [pg.Vector2(START_COL - col, START_ROW)
                     for col in range(START_LENGTH)]
        self.direction = pg.Vector2(1, 0)

        self.has_eaten = False

    def update(self):
        if not self.has_eaten:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.has_eaten = False

    def reset(self):
        self.body = [pg.Vector2(START_COL - col, START_ROW)
                     for col in range(START_LENGTH)]
        self.direction = pg.Vector2(1, 0)

    def draw(self):
        for point in self.body:
            rect = pg.Rect(point.x * TILE_SIZE, point.y * TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)
            pg.draw.rect(self.screen, 'red', rect)
