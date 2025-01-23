import random

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self, snake):
        self.vision = []
        self.reward = 0
        self.snake = snake

    def movement(self):
        # print(self.snake.direction, self.snake.state)
        if self.snake.direction.x == -1:
            return random.choice(['UP', 'RIGHT', 'DOWN'])
        elif self.snake.direction.x == 1:
            return random.choice(['UP', 'LEFT', 'DOWN'])
        elif self.snake.direction.y == -1:
            return random.choice(['LEFT', 'RIGHT', 'DOWN'])
        elif self.snake.direction.y == 1:
            return random.choice(['UP', 'RIGHT', 'LEFT'])
        else:
            return random.choice(['UP', 'RIGHT', 'LEFT', 'DOWN'])
