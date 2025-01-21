import contextlib
with contextlib.redirect_stdout(None):
    import pygame

import random
import os
from .config import SCREEN_WIDTH, SCREEN_HEIGHT, TIME_FONT, SCORE_FONT, GAME_NAME, WINDOW_POSITION, START_VELOCITY
from .player import Player
from .ball import Ball
from .network_client import NetworkClient


class Game:
    def __init__(self, player_name: str):
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{WINDOW_POSITION[0]},{WINDOW_POSITION[1]}"
        self.win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_NAME)

        self.server = NetworkClient()
        self.name = player_name
        self.current_id = None
        self.players: list[Player] = {}
        self.balls: list[Ball] = []
        self.game_time = 0
        self.clock = pygame.time.Clock()
        self.fps = 30

    @staticmethod
    def convert_time(t):
        if isinstance(t, str):
            return t
        minutes, seconds = divmod(int(t), 60)
        return f"{minutes}:{seconds:02}" if minutes else f"{seconds}s"

    def redraw_window(self):
        self.win.fill((255, 255, 255))

        # draw balls and players
        for ball in self.balls:
            ball.draw(self.win)
        for player in self.players.values():
            player.draw(self.win)

        title = TIME_FONT.render("Scoreboard", True, (0, 0, 0))
        self.win.blit(title, (SCREEN_WIDTH - title.get_width() - 10, 5))
        for count, player in enumerate(sorted(self.players.values(), key=lambda p: -p.score)[:3]):
            text = SCORE_FONT.render(f"{count + 1}. {player.name}", True, (0, 0, 0))
            self.win.blit(text, (SCREEN_WIDTH - title.get_width() - 10, 25 + count * 20))

        # Draw Timer and Current Player Score
        current_player = self.players[self.current_id]
        self.win.blit(TIME_FONT.render(f"Time: {self.convert_time(self.game_time)}", True, (0, 0, 0)), (10, 10))
        self.win.blit(TIME_FONT.render(f"Score: {round(current_player.score)}", True, (0, 0, 0)), (10, 40))

        pygame.display.update()

    def initialize_game(self):
        self.current_id = self.server.connect(self.name)
        balls_data, players_data, self.game_time = self.server.send("get")
        self.balls = [Ball(ball[0], ball[1], ball[2]) for ball in balls_data]
        self.players = {
            pid: Player(pid, pdata["x"], pdata["y"], pdata["color"], pdata["score"], pdata["name"])
            for pid, pdata in players_data.items()
        }

    def handle_movement(self):
        current_player = self.players[self.current_id]
        vel = max(START_VELOCITY - round(current_player.score / 14), 1)
        keys = pygame.key.get_pressed()
        current_player.move(keys, vel)

    def update_game_state(self):
        current_player = self.players[self.current_id]

        # send player's pos to server
        balls_data, players_data, self.game_time = self.server.send(
            f"move {current_player.x} {current_player.y}"
        )

        # Update balls
        self.balls = [Ball(ball[0], ball[1], ball[2]) for ball in balls_data]

        # Update players
        self.players = {
            pid: Player(pid, pdata["x"], pdata["y"], pdata["color"], pdata["score"], pdata["name"])
            for pid, pdata in players_data.items()
        }

    def run(self):
        run = True
        while run:
            self.clock.tick(self.fps)
            self.handle_movement()
            self.update_game_state()
            self.redraw_window()

            # poll events
            # Check for exit events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    run = False

        self.server.disconnect()
        pygame.quit()
        quit()
