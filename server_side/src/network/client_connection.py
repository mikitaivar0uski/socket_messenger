import socket

class ClientConnection:
    def __init__(self, socket: socket.socket):
        self.socket: socket.socket = socket

    def send_to_client(self, message: str) -> None:
        self.socket.send(message.encode())

    def receive_from_client(self) -> str:
        message = self.socket.recv(1024).decode().strip()
        return message

    def close_client_connection(self):
        self.socket.close()
