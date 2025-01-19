import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import random
import os
from network_client import NetworkClient

from typing import Dict, Tuple
from player import Player
from network_client import NetworkClient


# Constants
BALL_RADIUS = 5
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

def redraw_window(players, balls, game_time, score):
    WIN.fill((255, 255, 255))

    for ball in balls:
        pygame.draw.circle(WIN, ball[2], (ball[0], ball[1]), BALL_RADIUS)

    for player_id in sorted(players, key=lambda x: players[x]["score"]):
        p = players[player_id]
        pygame.draw.circle(WIN, p["color"], (p["x"], p["y"]), PLAYER_RADIUS + round(p["score"]))
        text = NAME_FONT.render(p["name"], True, (0, 0, 0))
        WIN.blit(text, (p["x"] - text.get_width() / 2, p["y"] - text.get_height() / 2))

    title = TIME_FONT.render("Scoreboard", True, (0, 0, 0))
    WIN.blit(title, (W - title.get_width() - 10, 5))

    for count, player_id in enumerate(sorted(players, key=lambda x: -players[x]["score"])[:3]):
        text = SCORE_FONT.render(f"{count + 1}. {players[player_id]['name']}", True, (0, 0, 0))
        WIN.blit(text, (W - title.get_width() - 10, 25 + count * 20))

    WIN.blit(TIME_FONT.render(f"Time: {convert_time(game_time)}", True, (0, 0, 0)), (10, 10))
    WIN.blit(TIME_FONT.render(f"Score: {round(score)}", True, (0, 0, 0)), (10, 40))
    
    pygame.display.update()

def handle_movement(keys, player, vel):
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player["x"] = max(player["x"] - vel, PLAYER_RADIUS + player["score"])
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player["x"] = min(player["x"] + vel, W - PLAYER_RADIUS - player["score"])
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player["y"] = max(player["y"] - vel, PLAYER_RADIUS + player["score"])
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player["y"] = min(player["y"] + vel, H - PLAYER_RADIUS - player["score"])

def main(name):
    server = NetworkClient()
    current_id = server.connect(name)
    balls, players, game_time = server.send("get")
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(30)
        player = players[current_id]
        vel = max(START_VEL - round(player["score"] / 14), 1)
        keys = pygame.key.get_pressed()
        handle_movement(keys, player, vel)
        balls, players, game_time = server.send(f"move {player['x']} {player['y']}")
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
                
        redraw_window(players, balls, game_time, player["score"])

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
