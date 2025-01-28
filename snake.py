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
        self.state = [0] * 12
        self.create_snake()

    def update(self, occupied, redApple):
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
        if not self.lose_by_length:
            self.update_vision(occupied, redApple)

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
        vision_matrix = [[" " for column in range(12)] for row in range(12)]
        head_y = int(self.body[0].y) + 1
        head_x = int(self.body[0].x) + 1
        vision_matrix[head_y][head_x] = 'H'

        vision_matrix[0][head_x] = 'W'
        vision_matrix[11][head_x] = 'W'
        vision_matrix[head_y][0] = 'W'
        vision_matrix[head_y][11] = 'W'

        for i in range(1, 11):
            if pg.Vector2(i - 1, head_y - 1) != pg.Vector2(head_x - 1, head_y - 1):
                vision_matrix[head_y][i] = '0'
                for apple in occupied:
                    if pg.Vector2(i - 1, head_y - 1) == apple.pos \
                            and apple.pos != r_apple.pos:
                        vision_matrix[head_y][i] = 'G'
                    elif pg.Vector2(i - 1, head_y - 1) == r_apple.pos:
                        vision_matrix[head_y][i] = 'R'
                if pg.Vector2(i - 1, head_y - 1) in self.body:
                    vision_matrix[head_y][i] = 'S'
            if pg.Vector2(head_x - 1, i - 1) != pg.Vector2(head_x - 1, head_y - 1):
                vision_matrix[i][head_x] = '0'
                for apple in occupied:
                    if pg.Vector2(head_x - 1, i - 1) == apple.pos \
                            and apple.pos != r_apple.pos:
                        vision_matrix[i][head_x] = 'G'
                    elif pg.Vector2(head_x - 1, i - 1) == r_apple.pos:
                        vision_matrix[i][head_x] = 'R'
                if pg.Vector2(head_x - 1, i - 1) in self.body:
                    vision_matrix[i][head_x] = 'S'
        self.get_state(vision_matrix)
        for row in vision_matrix:
            print("".join(row))

    # def update_state(self, r_b, r_end, primary_index, secondary_index, value):
    #     green_apple_found = False
    #     for i in range(r_b, r_end):
    #         if self.state[i] != 0:
    #             green_apple_found = True
    #     if green_apple_found is True:
    #         self.state[secondary_index] = value
    #     else:
    #         self.state[primary_index] = value

    def get_state(self, vision_matrix):
        head_y = int(self.body[0].y) + 1
        head_x = int(self.body[0].x) + 1
        self.state = [0] * 12

        for x in range(head_x + 1, len(vision_matrix[0])):
            if vision_matrix[head_y][x] == 'W' or vision_matrix[head_y][x] == 'S':
                self.state[1] = 1
                break
            elif vision_matrix[head_y][x] == 'G' or vision_matrix[head_y][x] == 'R':
                self.state[0] = 1
                break
            elif vision_matrix[head_y][x] == '0':
                self.state[2] = 1

        for x in range(head_x - 1, -1, -1):
            if vision_matrix[head_y][x] == 'W' or vision_matrix[head_y][x] == 'S':
                self.state[4] = 1
                break
            elif vision_matrix[head_y][x] == 'G' or vision_matrix[head_y][x] == 'R':
                self.state[3] = 1
                break
            elif vision_matrix[head_y][x] == '0':
                self.state[5] = 1

        for y in range(head_y + 1, len(vision_matrix)):
            if vision_matrix[y][head_x] == 'W' or vision_matrix[y][head_x] == 'S':
                self.state[7] = 1
                break
            elif vision_matrix[y][head_x] == 'G' or vision_matrix[y][head_x] == 'R':
                self.state[6] = 1
                break
            # elif vision_matrix[y][head_x] == 'R':
            #     self.state[9] = 1
            #     break
            elif vision_matrix[y][head_x] == '0':
                self.state[8] = 1

        for y in range(head_y - 1, -1, -1):
            if vision_matrix[y][head_x] == 'W' or vision_matrix[y][head_x] == 'S':
                self.state[10] = 1
                break
            elif vision_matrix[y][head_x] == 'G' or vision_matrix[y][head_x] == 'R':
                self.state[9] = 1
                break
            # elif vision_matrix[y][head_x] == 'R':
            #     self.state[13] = 1
            #     break
            elif vision_matrix[y][head_x] == '0':
                self.state[11] = 1

    # def get_state_for_neural(self, vision_matrix):
    #     head_y = int(self.body[0].y) + 1
    #     head_x = int(self.body[0].x) + 1

    #     self.state = [0] * 21

    #     # wall distance = 4 / body distance = 4/ good apple 1 et 2 = 8
    #     # direction = 1 et bad apple =4 donc 21
    #     def update_state(primary_index, secondary_index, value):
    #         green_apple_found = False
    #         for i in range(8, 12):
    #             if self.state[i] != 0:
    #                 green_apple_found = True
    #         if green_apple_found is True:
    #             self.state[secondary_index] = value
    #         else:
    #             self.state[primary_index] = value

    #     # Check horizontally (left-right)
    #     for x in range(len(vision_matrix[0])):
    #         dist = abs(head_x - x)
    #         if vision_matrix[head_y][x] == 'W':
    #             self.state[1 if head_x < x else 3] = dist
    #         elif vision_matrix[head_y][x] == 'S':
    #             self.state[5 if head_x < x else 7] = dist
    #         elif vision_matrix[head_y][x] == 'G':
    #             update_state(9 if head_x < x else 11, 13 if head_x < x else 15, dist)
    #         elif vision_matrix[head_y][x] == 'R':
    #             self.state[17 if head_x < x else 19] = dist

    #     # Check vertically (up-down)
    #     for y in range(len(vision_matrix)):
    #         dist = abs(head_y - y)
    #         if vision_matrix[y][head_x] == 'W':
    #             self.state[2 if head_y < y else 0] = dist
    #         elif vision_matrix[y][head_x] == 'S':
    #             if dist < self.state[6 if head_y < y else 4] or self.state[6 if head_y < y else 4] == 0:
    #                 self.state[6 if head_y < y else 4] = dist
    #         elif vision_matrix[y][head_x] == 'G':
    #             update_state(10 if head_y < y else 8, 14 if head_y < y else 12, dist)
    #         elif vision_matrix[y][head_x] == 'R':
    #             self.state[18 if head_y < y else 16] = dist

    #     if self.direction == pg.Vector2(0, -1):
    #         self.state[20] = 1
    #     elif self.direction == pg.Vector2(1, 0):
    #         self.state[20] = 2
    #     elif self.direction == pg.Vector2(0, 1):
    #         self.state[20] = 3
    #     elif self.direction == pg.Vector2(-1, 0):
    #         self.state[20] = 4
    #     print(self.state)