import socket
import pickle

class NetworkClient:
    def __init__(self, server="10.237.29.206", port=5555):
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.client = self._create_socket()

    def _create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, name):
        try:
            self.client.connect(self.addr)
            self.client.sendall(name.encode())
            val = self.client.recv(8)
            return int(val.decode())
        except (socket.error, ValueError) as e:
            print(f"Connection error: {e}")
            return None

    def disconnect(self):
        self.client.close()

    def send(self, data, use_pickle=False):
        try:
            serialized_data = pickle.dumps(data) if use_pickle else str(data).encode()
            self.client.sendall(serialized_data)
            reply = self.client.recv(8192)
            try:
                return pickle.loads(reply)
            except (pickle.UnpicklingError, EOFError):
                return reply.decode(errors='ignore')
        except socket.error as e:
            print(f"Send error: {e}")
            return None