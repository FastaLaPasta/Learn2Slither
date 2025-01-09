from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, COLS, ROWS
import pygame as pg
from snake import Snake
from apple import Apple


class game():
    def __init__(self):
        # general
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # game object
        self.bg_rect = [pg.Rect((col + int(row % 2 == 0)) * TILE_SIZE,
                                row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        for col in range(0, 10, 2) for row in range(10)]
        self.snake = Snake()
        self.apple = Apple(self.snake)

        # timer
        self.update_event = pg.event.custom_type()
        pg.time.set_timer(self.update_event, 110)
        self.game_active = True

    def draw_bg(self):
        self.screen.fill('lightgreen')
        for rect in self.bg_rect:
            pg.draw.rect(self.screen, 'darkgreen', rect)

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d] and self.snake.direction.x != -1:
            self.snake.direction = pg.Vector2(1, 0)
        if keys[pg.K_a] and self.snake.direction.x != 1:
            self.snake.direction = pg.Vector2(-1, 0)
        if keys[pg.K_w] and self.snake.direction.y != 1:
            self.snake.direction = pg.Vector2(0, -1)
        if keys[pg.K_s] and self.snake.direction.y != -1:
            self.snake.direction = pg.Vector2(0, 1)

    def collision(self):
        # apple
        if self.snake.body[0] == self.apple.pos:
            self.snake.has_eaten = True
            self.apple.set_pos()

        # game over
        if self.snake.body[0] in self.snake.body[1:] or \
            not 0 <= self.snake.body[0].x < COLS or \
                not 0 <= self.snake.body[0].y < ROWS:
            self.snake.reset()
            self.game_active = False

    def play(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
                if event.type == self.update_event and self.game_active:
                    self.snake.update()

                if event.type == pg.KEYDOWN and not self.game_active:
                    self.game_active = True
            # update
            self.input()
            self.collision()

            # drawing
            self.draw_bg()
            self.snake.draw()
            self.apple.draw()
            pg.display.flip()


main = game()
main.play()
