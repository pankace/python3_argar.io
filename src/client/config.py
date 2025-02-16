import pygame

# GAME Name
GAME_NAME = "Blobs"

# Screen Dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 830

MASS_LOSS_TIME = 7
ROUND_TIME = 60 * 5

# Player Constants
PLAYER_RADIUS = 10
START_VELOCITY = 9
START_RADIUS = 7

# Ball Constants
BALL_RADIUS = 5

# Colors
COLORS = [
    (255, 0, 0),
    (255, 128, 0),
    (255, 255, 0),
    (128, 255, 0),
    (0, 255, 0),
    (0, 255, 128),
    (0, 255, 255),
    (0, 128, 255),
    (0, 0, 255),
    (128, 0, 255),
    (255, 0, 255),
    (255, 0, 128),
    (128, 128, 128),
    (0, 0, 0),
]

# Fonts
pygame.font.init()
NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

# Window Position
WINDOW_POSITION = (0, 30)

# SEVER
PORT = 5555

# LOGGER
MAX_BYTES = 1_000_000  # 1MB
BACKUP_COUNT = 3
