import pygame

from pygame.surface import Surface
from pygame.key import ScancodeWrapper
from typing import Tuple


# Constants
PLAYER_RADIUS = 10
START_VEL = 9
W, H = 1600, 830  # Game screen dimensions

class Player:
    def __init__(
            self,
            player_id: int,
            x: int,
            y: int,
            color: Tuple[int, int, int],
            score: float = 0,
            name: str = "Player"
            ) -> None:
        self.id = player_id
        self.x = x
        self.y = y
        self.color = color
        self.score = score
        self.name = name

    def move(self, keys: ScancodeWrapper, vel: int) -> None:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x = max(self.x - vel, PLAYER_RADIUS + self.score)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x = min(self.x + vel, W - PLAYER_RADIUS - self.score)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y = max(self.y - vel, PLAYER_RADIUS + self.score)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y = min(self.y + vel, H - PLAYER_RADIUS - self.score)

    def draw(self, window: Surface) -> None:
        pygame.draw.circle(window, self.color, (self.x, self.y), PLAYER_RADIUS + round(self.score))
        name_font = pygame.font.SysFont("comicsans", 20)
        text = name_font.render(self.name, True, (0, 0, 0))
        # make a draw call
        window.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))
