import socket
import threading
import pickle
import time
import random
import math

# Constants
PORT = 5555
BALL_RADIUS = 5
START_RADIUS = 7
ROUND_TIME = 60 * 5
MASS_LOSS_TIME = 7
W, H = 1600, 830
COLORS = [
    (255, 0, 0), (255, 128, 0), (255, 255, 0), (128, 255, 0),
    (0, 255, 0), (0, 255, 128), (0, 255, 255), (0, 128, 255),
    (0, 0, 255), (128, 0, 255), (255, 0, 255), (255, 0, 128),
    (128, 128, 128), (0, 0, 0)
]

# Server setup
HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((SERVER_IP, PORT))
    server_socket.listen()
    print(f"[SERVER] Server started on {SERVER_IP}:{PORT}")
except socket.error as e:
    print(f"[ERROR] {e}")
    exit()

# Game state
players = {}
balls = []
connections = 0
next_id = 0
start_game = False
start_time = 0
next_mass_loss = 1
game_time = "Starting Soon"

def release_mass():
    for player in players.values():
        if player["score"] > 8:
            player["score"] = math.floor(player["score"] * 0.95)

def check_collision():
    for player in players.values():
        px, py, pscore = player["x"], player["y"], player["score"]
        for ball in balls[:]:
            bx, by = ball[:2]
            if math.hypot(px - bx, py - by) <= START_RADIUS + pscore:
                player["score"] += 0.5
                balls.remove(ball)

def player_collision():
    sorted_players = sorted(players.items(), key=lambda item: item[1]["score"])
    for i, (id1, p1) in enumerate(sorted_players):
        for id2, p2 in sorted_players[i+1:]:
            if math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"]) < p2["score"] - p1["score"] * 0.85:
                p2["score"] = math.hypot(p2["score"], p1["score"])
                reset_player(id1)
                print(f"[GAME] {p2['name']} ate {p1['name']}")

def create_balls(n):
    while len(balls) < n:
        x, y = random.randint(0, W), random.randint(0, H)
        if all(math.hypot(x - p["x"], y - p["y"]) > START_RADIUS + p["score"] for p in players.values()):
            balls.append((x, y, random.choice(COLORS)))

def reset_player(player_id):
    players[player_id]["score"] = 0
    players[player_id]["x"], players[player_id]["y"] = get_safe_spawn()

def get_safe_spawn():
    while True:
        x, y = random.randint(0, W), random.randint(0, H)
        if all(math.hypot(x - p["x"], y - p["y"]) > START_RADIUS + p["score"] for p in players.values()):
            return x, y

def client_thread(conn, player_id):
    global connections, start_game, start_time, next_mass_loss
    try:
        name = conn.recv(16).decode("utf-8")
        print(f"[CONNECT] {name} joined.")
        spawn_x, spawn_y = get_safe_spawn()
        players[player_id] = {"x": spawn_x, "y": spawn_y, "color": COLORS[player_id % len(COLORS)], "score": 0, "name": name}
        conn.send(str(player_id).encode())

        while True:
            if start_game:
                elapsed = round(time.time() - start_time)
                if elapsed >= ROUND_TIME:
                    start_game = False
                elif elapsed // MASS_LOSS_TIME >= next_mass_loss:
                    next_mass_loss += 1
                    release_mass()

            data = conn.recv(32)
            if not data:
                break

            command = data.decode("utf-8").split()
            if command[0] == "move":
                players[player_id]["x"], players[player_id]["y"] = map(int, command[1:3])
                if start_game:
                    check_collision()
                    player_collision()
                    if len(balls) < 150:
                        create_balls(random.randint(100, 150))

            conn.send(pickle.dumps((balls, players, elapsed)))
            time.sleep(0.01)
    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        print(f"[DISCONNECT] {players[player_id]['name']} left.")
        connections -= 1
        players.pop(player_id, None)
        conn.close()

create_balls(random.randint(200, 250))
print("[GAME] Level initialized.")

while True:
    conn, addr = server_socket.accept()
    print(f"[CONNECTION] {addr} connected.")
    if addr[0] == SERVER_IP and not start_game:
        start_game = True
        start_time = time.time()
        print("[START] Game started.")
    threading.Thread(target=client_thread, args=(conn, next_id)).start()
    connections += 1
    next_id += 1
