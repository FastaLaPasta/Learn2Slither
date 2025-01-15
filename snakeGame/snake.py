from settings import TILE_SIZE, ROWS, COLS
import pygame as pg
from random import randrange


class Snake:
    def __init__(self):
        self.screen = pg.display.get_surface()
        self.body = []
        self.direction = pg.Vector2()

        self.has_eaten_green = False
        self.has_eaten_red = False
        self.lose_by_length = False
        self.create_snake()

    def update(self):
        if not self.has_eaten_green and not self.has_eaten_red:
            body_copy = self.body
            body_copy.insert(0, body_copy[0] + self.direction)
            body_copy = self.body[:-1]
            self.body = body_copy[:]
        elif self.has_eaten_green:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.has_eaten_green = False
        else:
            body_copy = self.body
            body_copy.insert(0, body_copy[0] + self.direction)
            body_copy = self.body[:-2]
            self.body = body_copy[:]
            self.has_eaten_red = False
            if len(body_copy) == 0:
                self.lose_by_length = True

    def create_snake(self):
        head_pos = pg.Vector2(randrange(2, COLS, 1), randrange(0, ROWS, 1))
        self.body.append(head_pos)

        for _ in range(2):
            while True:
                direction = randrange(4)
                if direction == 0:
                    x_pos = int(self.body[-1].x) - 1
                    y_pos = int(self.body[-1].y)
                elif direction == 1:
                    x_pos = int(self.body[-1].x) + 1
                    y_pos = int(self.body[-1].y)
                elif direction == 2:
                    x_pos = int(self.body[-1].x)
                    y_pos = int(self.body[-1].y) - 1
                elif direction == 3:
                    x_pos = int(self.body[-1].x)
                    y_pos = int(self.body[-1].y) + 1
                if 0 <= x_pos < COLS and 0 <= y_pos < ROWS:
                    new_pos = pg.Vector2(x_pos, y_pos)
                    if new_pos not in self.body:
                        self.body.append(new_pos)
                        break

    def reset(self):
        self.body = []
        self.create_snake()
        self.direction = pg.Vector2()
        self.lose_by_length = False

    def draw(self):
        for point in self.body:
            rect = pg.Rect(point.x * TILE_SIZE, point.y * TILE_SIZE,
                           TILE_SIZE, TILE_SIZE)
            if point is self.body[0]:
                pg.draw.rect(self.screen, 'darkblue', rect)
            else:
                pg.draw.rect(self.screen, 'blue', rect)

    def update_vision(self, occupied, r_apple):
        vision_matrix = [[" " for column in range(11)] for row in range(11)]
        
        head_y = int(self.body[0].y)
        head_x = int(self.body[0].x)

        vision_matrix[head_y][head_x] = 'H'
        vision_matrix[head_y][0] = 'W'
        vision_matrix[head_y][-1] = 'W'
        vision_matrix[0][head_x] = 'W'
        vision_matrix[-1][head_x] = 'W'
        for i in range(1, len(vision_matrix) - 1):
            if pg.Vector2(i, head_y) != pg.Vector2(head_x, head_y):
                vision_matrix[head_y][i] = '0'
                for apple in occupied:
                    if pg.Vector2(i, head_y) == apple.pos and apple.pos != r_apple.pos:
                        vision_matrix[head_y][i] = 'G'
                    elif pg.Vector2(i, head_y) == r_apple.pos:
                        vision_matrix[head_y][i] = 'R'
            if pg.Vector2(head_x, i) != pg.Vector2(head_x, head_y):
                vision_matrix[i][head_x] = '0'
                for apple in occupied:
                    if pg.Vector2(head_x, i) == apple.pos and apple.pos != r_apple.pos:
                        vision_matrix[i][head_x] = 'G'
                    elif pg.Vector2(head_x, i) == r_apple.pos:
                        vision_matrix[i][head_x] = 'R'

        for row in vision_matrix:
            print("".join(row))
