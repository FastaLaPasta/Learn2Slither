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
            action_map = {'UP': 0, 'DOWN': 1, 'LEFT': 2, 'RIGHT': 3}
            action = action_map[action]
        else:
            action = np.argmax(self.q_table[self.snake.state])
        return action

    def update_q_table(self, state, action, reward, next_state):
        print(reward)
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.gamma * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[self.snake.state][action]
        self.q_table[state][action] += self.alpha * td_error

    def movement(self):
        # print(self.snake.state, self.reward)
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

    def execute_action(self, action):
        # Map action to direction
        action_map = {0: 'UP', 1: 'DOWN', 2: 'LEFT', 3: 'RIGHT'}
        direction = action_map[action]
        self.snake.move(direction)

        next_state = self.snake.state
        done = self.snake.lose_by_length

        return next_state, done

    def train_loop(self):   
        num_episodes = 1000

        for episode in range(num_episodes):
            state = self.snake.state
            done = False

            while not done:
                action = self.choose_action()
                next_state, done = self.execute_action(action)
                self.update_q_table(state, action, self.reward, next_state)
                state = next_state
            self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

            if (episode + 1) % 100 == 0:
                print(f"Episode: {episode + 1}, Epsilon: {self.epsilon:.2f}")
