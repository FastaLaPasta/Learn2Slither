from random import choice


class Agent:
    def __init__(self):
        self.vision = []

    def movement(self):
        return choice(['UP', 'RIGHT', 'DOWN', 'LEFT'])
