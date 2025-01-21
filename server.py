from src.server import network_server

if __name__ == "__main__":
    server = network_server.NetworkServer()
    server.run()