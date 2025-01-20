import socket
import threading
import pickle
import time
import random
import math
import netifaces # dynamic ip selection
from config import PORT, START_RADIUS, COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, ROUND_TIME, MASS_LOSS_TIME

class NetworkUtils:
    @staticmethod
    def get_network_ip():
        try:
            for interface in netifaces.interfaces():
                # skip loopback
                if interface == "lo0":
                    continue
                addresses = netifaces.ifaddresses(interface)
                # check ipv4
                if netifaces.AF_INET in addresses:
                    ipv4_info = addresses[netifaces.AF_INET][0]
                    ip_address = ipv4_info['addr']
                    if not ip_address.startswith("127."):
                        return ip_address
        except Exception as e:
            print(f"Error occurred while fetching network IP: {e}")
        # fallback address
        return socket.gethostbyname(socket.gethostname())

class NetworkServer:
    def __init__(self):
        self.players = {}
        self.balls = []
        self.connections = 0
        self.next_id = 0
        self.start_game = False
        self.start_time = 0
        self.next_mass_loss = 1
        self.game_time = "Starting soon"
        self.server_ip = NetworkUtils.get_network_ip()
        self.server_socket = self._initialize_server()
        print(f"[SERVER] Server started on {self.server_ip}:{PORT}\nHost: {socket.gethostname()}")

    def _initialize_server(self):
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            try:
                server_socket.bind((self.server_ip, PORT))
                server_socket.listen()
            except socket.error as e:
                print(f"[ERROR] {e}")
                exit()
            return server_socket

    def release_mass(self):
        # gradually reduce the score of players
        for player in self.players.values():
            if player["score"] > 8:
                player["score"] = math.floor(player["score"] * 0.95)

    def check_collision(self, player_id):
        player = self.players[player_id]
        for ball in self.balls[:]:
            if math.hypot(player["x"] - ball[0], player["y"] - ball[1]) <= START_RADIUS + player["score"]:
                player["score"] += 0.5
                self.balls.remove(ball)

    def player_collision(self):
        sorted_players = sorted(self.players.items(), key=lambda item: item[1]["score"])
        for i, (id1, p1) in enumerate(sorted_players):
            for id2, p2 in sorted_players[i+1:]:
                if math.hypot(p1["x"] - p2["x"], p1["y"] - p2["y"]) < p2["score"] - p1["score"] * 0.85:
                    p2["score"] = math.hypot(p2["score"], p1["score"])
                    self.reset_player(id1)
                    print(f"[GAME] {p2['name']} ate {p1['name']}")

    def create_balls(self, n):
        while len(self.balls) < n:
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            if all(math.hypot(x - p["x"], y - p["y"]) > START_RADIUS + p["score"] for p in self.players.values()):
                self.balls.append((x, y, random.choice(COLORS)))

    def reset_player(self, player_id):
        self.players[player_id]["score"] = 0
        self.players[player_id]["x"], self.players[player_id]["y"] = self.get_safe_spawn()

    def get_safe_spawn(self):
        # random position for spawning a player that does not collide with others.
        while True:
            x, y = random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)
            if all(math.hypot(x - p["x"], y - p["y"]) > START_RADIUS + p["score"] for p in self.players.values()):
                return x, y

    def client_thread(self, conn, player_id):
        try:
            name = conn.recv(16).decode("utf-8")
            print(f"[CONNECT] {name} joined.")
            spawn_x, spawn_y = self.get_safe_spawn()
            self.players[player_id] = {"x": spawn_x, "y": spawn_y, "color": COLORS[player_id % len(COLORS)], "score": 0, "name": name}
            conn.send(str(player_id).encode())

            while True:
                if self.start_game:
                    elapsed = round(time.time() - self.start_time)
                    if elapsed >= ROUND_TIME:
                        self.start_game = False
                    elif elapsed // MASS_LOSS_TIME >= self.next_mass_loss:
                        self.next_mass_loss += 1
                        self.release_mass()

                data = conn.recv(32)
                if not data:
                    break

                command = data.decode("utf-8").split()
                if command[0] == "move":
                    self.players[player_id]["x"], self.players[player_id]["y"] = map(int, command[1:3])
                    if self.start_game:
                        self.check_collision(player_id)
                        self.player_collision()
                        if len(self.balls) < 150:
                            self.create_balls(random.randint(100, 150))

                conn.send(pickle.dumps((self.balls, self.players, elapsed)))
                time.sleep(0.01)
        except Exception as e:
            print(f"[ERROR] {e}")
        finally:
            print(f"[DISCONNECT] {self.players[player_id]['name']} left.")
            self.connections -= 1
            self.players.pop(player_id, None)
            conn.close()

    def run(self):
        self.create_balls(random.randint(200, 250))
        print("[GAME] Level initialized.")

        while True:
            conn, addr = self.server_socket.accept()
            print(f"[CONNECTION] {addr} connected.")
            if addr[0] == self.server_ip and not self.start_game:
                self.start_game = True
                self.start_time = time.time()
                print("[START] Game started.")
            threading.Thread(target=self.client_thread, args=(conn, self.next_id)).start()
            self.connections += 1
            self.next_id += 1


if __name__ == "__main__":
    server = NetworkServer()
    server.run()