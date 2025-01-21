from random import choice


class Agent:
    def __init__(self):
        self.vision = []
        self.reward = 0

    def movement(self):
        return choice(['UP', 'RIGHT', 'DOWN', 'LEFT'])
