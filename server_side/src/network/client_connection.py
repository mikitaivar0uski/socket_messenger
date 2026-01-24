import socket

class ClientNetwork():
    def __init__(self, socket: socket.socket):
        self.socket: socket.socket = socket

    def sent_to_client(self, message: str) -> None:
        socket.send(message.encode())

    def receive_from_client(self) -> str:
        message = socket.recv(1024).decode()
        return message

    def close_client_connection(self):
        socket.close()