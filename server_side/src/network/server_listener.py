import socket

from server_side.src.network.client_connection import ClientNetwork

class ServerNetwork():
    def __init__(self):
        self.server_ip: str
        self.server_port: int
        self.listening_socket: socket.socket
        self.running = True

    def start_listening(self):
        self.listening_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # ipv4 + tcp

        self._listening_socket.bind(self.server_ip, self.server_port)
        self._listening_socket.listen(20)

    def accept_connections(self):
        client_socket, client_ip = self.listening_socket.accept()
        connection = ClientNetwork(client_socket)
        return connection

    def stop_listening(self):
        self.listening_socket.close()