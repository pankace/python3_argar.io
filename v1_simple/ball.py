import pygame

from pygame.surface import Surface
from typing import Tuple


# constants
BALL_RADIUS = 5

class Ball:
    def __init__(
            self,
            x: int,
            y: int,
            color: Tuple[int, int, int]
        ) -> None:
        self.x = x
        self.y = y
        self.color = color

    def draw(self, window: Surface, radius: int) -> None:
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
