# Python3 Agar.io

## 0. Team Contributions

- **Tanis**: Developed the core game logic and mechanics.
- **Nyein Chan**: Refactored the code and cleaned up the repository.
- **Aleksandre Nadirashvili**: Contributed ideas and math related to movement, food generation, and spawn points.

---

## 1. Introduction

This is a Python-based multiplayer server for a game inspired by **Agar.io**. In this game, players control entities that grow by consuming smaller objects (or other players).

---

## 2. Usage

1. **Run the Server**: Start the server by running the `network_server.py` file:
   
   ```bash
   python .\network_server.py
   ```

2. **Run the Game**: Each player on the local network needs to run the `app.py` file on their own computer:
   
   ```bash
   python .\app.py
   ```
---

## 3. Features

### **Key Features:**
1. **Multiplayer**: 
   - Supports multiple players over a local network.
   - Each player has a unique ID and color.

2. **Game Mechanics**: 
   - Players grow by eating smaller balls or other players.
   - Larger players can consume smaller ones, combining scores.
   - Player mass decreases over time to avoid indefinite growth.

3. **Server Setup**: 
   - The server uses Python’s `socket` library for connections.
   - Each client runs in its own thread to allow simultaneous play.
   - Game data is sent using Python's `pickle` module for serialization.

4. **Dynamic Game State**: 
   - The server maintains a central game state, tracking players' positions, scores, colors, and ball locations.

---

## 4. Code Breakdown

### **Game Components:**

- **`Player` Class**: 
   - Manages player details like position, color, score, and size.
   - Players move using keyboard inputs and grow by eating objects.
  
- **`Ball` Class**: 
   - Represents collectible balls that players can eat to gain score.

- **`Game` Class**: 
   - Controls the game loop, player movements, and game state updates.
   - Connects to the server and updates scores, positions, etc.

- **`NetworkClient` Class**: 
   - Manages client-server communication for movement and game data updates.

- **`NetworkServer` Class**: 
   - Handles game logic on the server side, such as tracking player positions, handling collisions, and managing multiple clients.
   
- **`NetworkUtils` Class**: 
   - Provides utility functions to fetch the server's IP dynamically.

---

### **Game Logic**:
- **Ball Creation**: Ensures new balls are placed in safe spots away from players.
- **Collisions**: Detects when players collide with balls or other players, updating scores accordingly.
- **Player Management**: Includes functions for spawning players safely and resetting them after they are consumed.
- **Mass Decay**: Reduces player mass over time to prevent continuous growth.

---

### **Server and Client Communication**:
- Each client is handled in a separate thread to allow multiple players to interact simultaneously.
- The server manages player movement, score updates, and ball generation.

---

## 5. Additional Notes

1. **Scalability**: 
   - The server can handle many players, but performance depends on hardware and network quality.

2. **Thread Safety**: 
   - Some data structures are not thread-safe, which could cause issues under high load.

3. **Security**: 
   - The use of `pickle` for data serialization could be risky.

4. **Improvements**: 
   - Implement locking mechanisms to avoid race conditions.
   - Add error handling for unexpected client disconnections.
   - Enhance security by validating inputs and avoiding direct `pickle` usage.

---

## 6. Core Game Features

- **Movement**: Players move around using keyboard inputs, and their size changes based on their score.
- **Ball Collection**: Players collect balls to grow their size. The server manages ball creation and collisions.
- **Player Collision**: Larger players can consume smaller players, resetting their score and causing respawn.
- **Network Communication**: The server keeps track of the game state and synchronizes with clients. Clients send movement data, which the server processes.

---
