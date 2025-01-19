import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import random
import os

from player import Player, START_VEL
from ball import Ball, BALL_RADIUS
from network_client import NetworkClient


# Constants
W, H = 1600, 830

# Fonts
pygame.font.init()
NAME_FONT = pygame.font.SysFont("comicsans", 20)
TIME_FONT = pygame.font.SysFont("comicsans", 30)
SCORE_FONT = pygame.font.SysFont("comicsans", 26)

# Colors
COLORS = [
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0),
    (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128),
    (128, 128, 128), (0, 0, 0)
]

# Initialize Pygame window
os.environ['SDL_VIDEO_WINDOW_POS'] = "0,30"
WIN = pygame.display.set_mode((W, H))
pygame.display.set_caption("Blobs")

def convert_time(t):
    if isinstance(t, str):
        return t
    minutes, seconds = divmod(int(t), 60)
    return f"{minutes}:{seconds:02}" if minutes else f"{seconds}s"

def redraw_window(
        players: dict[int, Player], 
        balls, 
        game_time: int,
        current_id: int,
        ):
    WIN.fill((255, 255, 255))

    for ball in balls:
        ball.draw(WIN, BALL_RADIUS)
    for player in players.values():
        player.draw(WIN)

    # draw scoreboard
    title = TIME_FONT.render("Scoreboard", True, (0, 0, 0))
    WIN.blit(title, (W - title.get_width() - 10, 5))
    for count, player in enumerate(sorted(players.values(), key=lambda p: -p.score)[:3]):
        text = SCORE_FONT.render(f"{count + 1}. {player.name}", True, (0, 0, 0))
        WIN.blit(text, (W - title.get_width() - 10, 25 + count * 20))

    # Draw Timer and Current Player Score
    current_player = players[current_id]
    WIN.blit(TIME_FONT.render(f"Time: {convert_time(game_time)}", True, (0, 0, 0)), (10, 10))
    WIN.blit(TIME_FONT.render(f"Score: {round(current_player.score)}", True, (0, 0, 0)), (10, 40))

    pygame.display.update()

def main(name: str):
    server = NetworkClient()
    current_id = server.connect(name)
    balls_data, players_data, game_time = server.send("get")

    # ball objects
    balls = [Ball(ball[0], ball[1], ball[2]) for ball in balls_data]

    # player objects
    players = {
        pid: Player(pid, pdata["x"],
            pdata["y"],
            pdata["color"],
            pdata["score"],
            pdata["name"]
    ) for pid, pdata in players_data.items()}

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        current_player = players[current_id]
        vel = max(START_VEL - round(current_player.score / 14), 1)

        # player movement
        keys = pygame.key.get_pressed()
        current_player.move(keys, vel)

        # update game states
        balls_data, players_data, game_time = server.send(
            f"move {current_player.x} {current_player.y}"
        )
        balls = [Ball(ball[0], ball[1], ball[2]) for ball in balls_data]

        players = {
            pid: Player(pid, pdata["x"],
                pdata["y"],
                pdata["color"],
                pdata["score"],
                pdata["name"]
            ) for pid, pdata in players_data.items()
        }

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False

        redraw_window(players, balls, game_time, current_id)

    server.disconnect()
    pygame.quit()
    quit()

if __name__ == "__main__":
    while True:
        name = input("Please enter your name (1-19 characters): ")
        if 1 <= len(name) <= 19:
            break
        print("Invalid name length. Try again.")
    main(name)
