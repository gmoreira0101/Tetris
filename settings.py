import pygame

#Game size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 40
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

#Side bar size
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

#window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

#game behaviour
UPDATE_START_SPEED = 800
MOVE_WAIT_TIME = 200
ROTATE_WAIT_TIME = 200
BLOCK_OFFSET = pygame.Vector2(COLUMNS // 2, -1)

#Cores
GRAY = (28, 28, 28)           # '#1C1C1C'
LINE_COLOR = (255, 255, 255)  # '#FFFFFF'
RED = (229, 27, 32)           # '#e51b20'
PURPLE = (123, 33, 127)       # '#7b217f'
CYAN = (108, 198, 217)        # '#6cc6d9'
ORANGE = (240, 126, 19)       # '#f07e13'
BLUE = (32, 75, 155)          # '#204b9b'
YELLOW = (241, 230, 13)       # '#f1e60d'
GREEN = (101, 179, 46)        # '#65b32e'


#Shapes
TETROMINOS = {
    'T' : {'shape': [(0,0), (-1,0), (1,0), (0,-1)], 'color': PURPLE},
    'O' : {'shape': [(0,0), (0,-1), (1,0), (1,-1)], 'color': YELLOW},
    'J' : {'shape': [(0,0), (0,-1), (0,1), (-1,1)], 'color': BLUE},
    'L' : {'shape': [(0,0), (0,-1), (0,1), (1,1)], 'color': ORANGE},
    'I' : {'shape': [(0,0), (0,-1), (0,-2), (0,1)], 'color': CYAN},
    'S' : {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color': GREEN},
    'Z' : {'shape': [(0,0), (1,0), (0,-1), (-1,-1)], 'color': RED}
}

SCORE_DATA = {1: 40, 2: 100, 3: 300, 4:1200}