import pygame as pg


class snake:
    def init(self):
        self.WINDOW = 1000
        self.TILE_SIZE = 50
        self.clock = pg.time.Clock()
        self.snake_dir = (0, 0)
        self.time, self.time_step = 0, 110
        self.snake = pg.Rect(0, 0, self.TILE_SIZE, self.TILE_SIZE)

    def movements(self, key):
        if key[pg.K_w] is True:
            self.snake_dir = (0, -(self.TILE_SIZE))
        elif key[pg.K_s] is True:
            self.snake_dir = (0, self.TILE_SIZE)
        elif key[pg.K_a] is True:
            self.snake_dir = (-(self.TILE_SIZE), 0)
        elif key[pg.K_d] is True:
            self.snake_dir = (self.TILE_SIZE, 0)

    def collision(self):
        if self.snake.top < 0:
            print('1')
        elif self.snake.bottom > self.WINDOW:
            print('2')
        elif self.snake.left < 0:
            print('3')
        elif self.snake.right > self.WINDOW:
            print('4')
        else:
            print('hahahaha')

    def display(self):
        screen = pg.display.set_mode([self.WINDOW] * 2)

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            pg.draw.rect(screen, 'green', self.snake)

            key = pg.key.get_pressed()
            self.movements(key)
            self.collision()
            time_now = pg.time.get_ticks()
            if time_now - self.time > self.time_step:
                self.time = time_now
                self.snake.move_ip(self.snake_dir)
            pg.display.flip()

game = snake()
game.init()
game.display()
