from random import randrange

TILE_SIZE = 100
ROWS = 10
COLS = 10
WINDOW_WIDTH = ROWS * TILE_SIZE
WINDOW_HEIGHT = COLS * TILE_SIZE

# start position
START_LENGTH = 3
START_ROW = randrange(0, ROWS, 1)
START_COL = randrange(2, COLS, 1)
