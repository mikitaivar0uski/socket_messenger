import os
import socket
from dotenv import load_dotenv
from client_side.src.network.network_handler import NetworkHandler


class SocketsNetworkHandler(NetworkHandler):
    def __init__(
        self,
        server_address: str = os.getenv("SERVER_ADDRESS"),
        server_port: int = int(os.getenv("SERVER_PORT")),
    ):
        self.socket: socket.socket = None
        self.server_address = server_address
        self.server_port = server_port

    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.server_port))
        return

    def send(self, message):
        return super().send(message)

    def receive(self):
        return super().receive()

    def close_connection(self):
        return super().close_connection()
