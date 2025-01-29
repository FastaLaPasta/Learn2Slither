from settings import WINDOW_WIDTH, WINDOW_HEIGHT, TILE_SIZE, COLS, ROWS
import pygame as pg
from snake import Snake
from apple import GreenApple, RedApple
from agent import Agent


class game():
    def __init__(self):
        # general
        self.screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        # game object
        self.bg_rect = [pg.Rect((col + int(row % 2 == 0)) * TILE_SIZE,
                                row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        for col in range(0, 10, 2) for row in range(10)]
        self.snake = Snake()
        self.greenApples = [GreenApple(self.snake) for i in range(2)]
        self.redApple = RedApple(self.snake, self.greenApples)
        self.occupied = self.greenApples + [self.redApple]
        for apple in self.greenApples:
            apple.get_occupied_tile(self.occupied)
        self.snake.update_vision(self.occupied, self.redApple)
        self.agent = Agent(self.snake)

        # timer
        self.update_event = pg.event.custom_type()
        pg.time.set_timer(self.update_event, 15)
        self.game_active = False

    def draw_bg(self):
        self.screen.fill('lightgrey')
        for rect in self.bg_rect:
            pg.draw.rect(self.screen, 'darkgrey', rect)

    def input(self, movement):
        # keys = pg.key.get_pressed()
        # if keys[pg.K_d] and self.snake.direction.x != -1:
        #     self.snake.direction = pg.Vector2(1, 0)
        # if keys[pg.K_a] and self.snake.direction.x != 1:
        #     self.snake.direction = pg.Vector2(-1, 0)
        # if keys[pg.K_w] and self.snake.direction.y != 1:
        #     self.snake.direction = pg.Vector2(0, -1)
        # if keys[pg.K_s] and self.snake.direction.y != -1:
        #     self.snake.direction = pg.Vector2(0, 1)
        if movement == 3 and self.snake.direction.x != -1:
            self.snake.direction = pg.Vector2(1, 0)
        if movement == 2 and self.snake.direction.x != 1:
            self.snake.direction = pg.Vector2(-1, 0)
        if movement == 0 and self.snake.direction.y != 1:
            self.snake.direction = pg.Vector2(0, -1)
        if movement == 1 and self.snake.direction.y != -1:
            self.snake.direction = pg.Vector2(0, 1)
        # print(movement)

    def respawn(self):
        self.snake.reset()
        for apple in self.occupied:
            apple.set_pos()
        self.snake.update_vision(self.occupied, self.redApple)

    def collision(self):
        # game over
        if self.snake.lose_by_length:
            self.agent.reward = -10

            self.respawn()
            self.game_active = True
            return True
        elif (not 0 <= self.snake.body[0].x < COLS or
              not 0 <= self.snake.body[0].y < ROWS or
                self.snake.body[0] in self.snake.body[1:]):
            self.agent.reward = -10
            self.respawn()
            self.game_active = True
            return True

        # apple
        for apple in self.greenApples:
            if self.snake.body[0] == apple.pos:
                self.snake.has_eaten_green = True
                self.agent.reward = 10
                apple.set_pos()

        if self.snake.body[0] == self.redApple.pos:
            self.snake.has_eaten_red = True
            self.agent.reward = 10
            self.redApple.set_pos()
        if self.agent.reward == 0:
            self.agent.reward = -0.1

    def play(self):
        num_episodes = 1000
        length = [0]
        for episode in range(num_episodes):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()
            done = False
            self.agent.reward = 0

            while not done:
                action = self.agent.choose_action()
                state = self.snake.get_state()
                self.input(self.agent.choose_action())
                self.snake.update(self.occupied, self.redApple)
                next_state = self.snake.get_state()
                done = self.collision()
                self.agent.update_q_table(state, action, self.agent.reward, next_state)
                self.draw_bg()
                self.snake.draw()
                for apple in self.greenApples:
                    apple.draw()
                self.redApple.draw()
                pg.display.flip()
                if (len(self.snake.body) > max(length)):
                    length.append(len(self.snake.body))
            # self.agent.epsilon = max(self.agent.epsilon_min, self.agent.epsilon * self.agent.epsilon_decay)
        print(max(length))
        # while True:
        #     for event in pg.event.get():
        #         if event.type == pg.QUIT:
        #             pg.quit()
        #             exit()
        #         if event.type == self.update_event and self.game_active:
        #             self.input(self.agent.choose_action())
        #             self.snake.update(self.occupied, self.redApple)
        #             self.collision()

        #         if event.type == pg.KEYDOWN and not self.game_active:
        #             self.game_active = True
        #     # drawing
        #     self.draw_bg()
        #     self.snake.draw()
        #     for apple in self.greenApples:
        #         apple.draw()
        #     self.redApple.draw()
        #     pg.display.flip()


main = game()
main.play()
