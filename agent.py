import random
import numpy as np

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self, snake):
        self.vision = []
        self.reward = 0
        self.snake = snake

        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.gamma = 0.9
        self.alpha = 0.1
        self.q_table = np.zeros((2 ** len(self.snake.state), 4))
        print(self.snake.state, self.reward)

    def choose_action(self):
        if random.random() < self.epsilon:
            action = self.movement()
        else:
            action = np.argmax(self.q_table[self.snake.state])
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
        return action

    def movement(self):
        print(self.snake.state, self.reward)
        if self.snake.direction.x == -1:
            return random.choice(['UP', 'RIGHT', 'DOWN'])
        elif self.snake.direction.x == 1:
            return random.choice(['UP', 'LEFT', 'DOWN'])
        elif self.snake.direction.y == -1:
            return random.choice(['LEFT', 'RIGHT', 'DOWN'])
        elif self.snake.direction.y == 1:
            return random.choice(['UP', 'RIGHT', 'LEFT'])
        else:
            return random.choice(['UP', 'RIaGHT', 'LEFT', 'DOWN'])
