import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_RADIUS, NAME_FONT, START_VELOCITY
from pygame.surface import Surface
from pygame.key import ScancodeWrapper
from typing import Tuple, Optional
from client_logger import logger as client_logger

class Player:
    def __init__(
            self,
            player_id: int,
            x: int,
            y: int,
            color: Tuple[int, int, int],
            score: float = 0,
            name: Optional[str] = "Player"
            ) -> None:
        self.id = player_id
        self.x = x
        self.y = y
        self.color = color
        self.score = score
        self.name = name

    @property
    def radius(self) -> int:
        return PLAYER_RADIUS + round(self.score)

    def move(self, keys: ScancodeWrapper, vel: int) -> None:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            client_logger.debug(f"Player {self.name} moved left")
            self.x = max(self.x - vel, self.radius)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            client_logger.debug(f"Player {self.name} moved right")
            self.x = min(self.x + vel, SCREEN_WIDTH - self.radius)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            client_logger.debug(f"Player {self.name} moved up")
            self.y = max(self.y - vel, self.radius)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            client_logger.debug(f"Player {self.name} moved down")
            self.y = min(self.y + vel, SCREEN_HEIGHT - self.radius)

    def draw(self, window: Surface) -> None:
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)
        text = NAME_FONT.render(self.name, True, (0, 0, 0))
        # make a draw call
        window.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "color": self.color,
            "score": self.score,
            "name": self.name,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        return cls(
            player_id=data["id"],
            x=data["x"],
            y=data["y"],
            color=tuple(data["color"]),
            score=data["score"],
            name=data["name"],
        )
