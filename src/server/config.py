import pygame


# Screen Dimensions
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 830

MASS_LOSS_TIME = 7
ROUND_TIME = 60 * 5

# Player Constants
PLAYER_RADIUS = 10
START_VELOCITY = 9
START_RADIUS = 7


# Colors
COLORS = [
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0),
    (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128),
    (128, 128, 128), (0, 0, 0)
]

# SEVER
PORT = 5555

# LOGGER
MAX_BYTES = 1_000_000  # 1MB
BACKUP_COUNT = 3