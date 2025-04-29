import os

import pygame
import win32api
from win32api import GetSystemMetrics
from button import Button
# Screen dimensions

SCR_HEIGHT = GetSystemMetrics(1)
SCR_WIDTH = GetSystemMetrics(0)
BOARD_HEIGHT = int(SCR_HEIGHT / 1.35)
BOARD_WIDTH = BOARD_HEIGHT
BOARD_START_Y = (SCR_HEIGHT - BOARD_HEIGHT) // 2
BOARD_START_X = (SCR_WIDTH - BOARD_WIDTH) // 2

# Board dimensions
COLS = 8
ROWS = 8
SQSIZE = BOARD_WIDTH // COLS
PIECE_SIZE = int(SQSIZE * 0.9)
SELECTED_PIECE_SIZE = PIECE_SIZE * 1.5
BORDER_RADIUS = 15
SIDEBAR_WIDTH = SCR_WIDTH // 5
SETTING_BTN_WIDTH = 80
TIME_CONTROL_BTN_Y_OFFSET = BORDER_RADIUS * 6


GREEN = (105, 146, 62)
DARK_GREEN = (78, 120, 55)
GRAY = (75, 72, 71)
DARK_GRAY = (44, 43, 41)
RED = (255, 100, 100)
SELECT_CIRCLE_COLOR = (125, 125, 125)
DARKER_GRAY = (25, 25, 25)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SOUNDS_DIR = os.path.join(PROJECT_ROOT, 'assets', 'sounds')
IMAGE_DIR = os.path.join(PROJECT_ROOT, 'assets', 'images')

exit_image = pygame.transform.scale(
    pygame.image.load("../assets/images/close_btn.png"),
    (20, 20)
)

minimize_image = pygame.transform.scale(
    pygame.image.load("../assets/images/minimize_btn.png"),
    (20, 20)
)


# Config
LIGHT_SQUARE_COLOR = 234, 235, 200
DARK_SQUARE_COLOR = 119, 154, 88
VALID_MOVE_COLOR = (125, 125, 125)
VALID_MOVE_COLOR_DARK = (100, 100, 100)
DEFAULT_LIGHT_TRACE = (244, 247, 116)
LAST_MOVE_INDICATOR_COLOR_DARK = (172, 195, 51)
MOVE_OPTION_STYLE = "Circle", "Square", "None"
MOVE_OPTION_COLOR = DARK_GRAY
HOVERED_SQUARE_COLOR = (180, 180, 180)
