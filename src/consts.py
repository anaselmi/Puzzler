# Colors & Pallets
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
D_GREY = (200, 200, 200)
M_GREY = (150, 150, 150)
BEIGE = (222, 184, 135)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
D_GREEN = (62, 81, 74)
L_GREEN = (101, 110, 85)
BLUE = (0, 0, 255)
D_BLUE = (63, 68, 80)

FG = WHITE
BG = BLACK

PLT_WB = WHITE, BLACK
PLT_F = M_GREY, BLACK


# Screen Parameters
FPS = 60
# Milliseconds per frame.
MS_PER_FRAME = 1000 / 60
FULLSCREEN = False
GREYSCALE = True
ALT_LAYOUT = True

W = 113
H = 40
SIZE = W, H
CENTER_X = W // 2
CENTER_Y = H // 2

LOG = "log"
LOG_BASE_WIDTH = W
LOG_BASE_HEIGHT = 10 + 2
LOG_BASE_SIZE = LOG_BASE_WIDTH, LOG_BASE_HEIGHT
LOG_WIDTH = LOG_BASE_WIDTH + 2
LOG_HEIGHT = LOG_BASE_HEIGHT + 2
LOG_SIZE = LOG_WIDTH, LOG_HEIGHT

TILE = "map"
TILE_BASE_WIDTH = 81
TILE_BASE_HEIGHT = 26
TILE_BASE_SIZE = TILE_BASE_WIDTH, TILE_BASE_HEIGHT
TILE_WIDTH = TILE_BASE_WIDTH + 2
TILE_HEIGHT = TILE_BASE_HEIGHT + 2
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT

FRAME_W = FRAME_H = 1
FRAME_SIZE = FRAME_W, FRAME_H
FRAME_STRING = "?"


# Misc
TITLE = "Puzzler: The Roguelike"
FONT_PATH = "assets\\courier12x12.png"
FONT_SIZE = 12
START_MESSAGE = ["Welcome to Puzzler!"]

# Commands
C_K_MOVE = "move"
C_MOVE = {C_K_MOVE: None}
C_K_ENTER = "enter"
C_ENTER = {C_K_ENTER: True}
C_K_EXIT = "enter"
C_EXIT = {C_K_EXIT: True}
C_K_RETURN = "return"
C_RETURN = {C_K_RETURN: True}
C_K_LOOK = "look"
C_LOOK = {C_K_LOOK: True}
C_K_CONSUMED = "consumed"
C_CONSUMED = {C_K_CONSUMED: True}

