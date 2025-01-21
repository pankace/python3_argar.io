import pygame

from .config import BALL_RADIUS
from pygame.surface import Surface
from typing import Tuple


class Ball:
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        self.x = x
        self.y = y
        self.color = color

    def draw(self, window: Surface) -> None:
        pygame.draw.circle(window, self.color, (self.x, self.y), BALL_RADIUS)

