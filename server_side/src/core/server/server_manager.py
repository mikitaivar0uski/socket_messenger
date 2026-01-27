# core functionality
import socket
import threading

# config
from dotenv import load_dotenv
import os

# typehinting
from typing import Callable

# internal modules
from core.client.client_states import ClientStates

from core.server.session_manager import SessionManager
from core.client.client_manager import ClientManager
from core.server.command_handler import CommandHandler

from network.server_listener import Listener
from network.client_connection import ClientConnection

load_dotenv()

# listen -> accept | Network
# -> threading | main
# -> handler (show menu and process commands) | CommandHandler
# -> session (optional) | SessionManager
# -> disconnect | main


class ServerManager:
    def __init__(
        self,
        server_ip: str = os.getenv("LISTENING_ADDRESS"),
        server_port: int = int(os.getenv("LISTENING_PORT")),
    ):

        self._server_ip = server_ip
        self._server_port = server_port

        self._client_server_connections: dict[str, ClientManager] = {}
        self._all_states: ClientStates = ClientStates
        self._all_sessions: dict[str, tuple[SessionManager, SessionManager]] = {}

    #### INIT CONNECTION ####
    def run(self):
        listener = Listener(self._server_ip, self._server_port)
        listener.start_listening()
        while listener.running:
            new_connection = listener.accept_connections()
            new_thread = threading.Thread(target=self.serve, 
                                          args=(new_connection,))
            new_thread.start()


    #### SERVE ####
    def serve(self, connection: ClientConnection):
        cl_manager = self.register_client(connection)
        try:
            cl_manager.run()
        except Exception as e:
            cl_manager.disconnect_client()

    #### REGISTER ####
    def register_client(self, connection: ClientConnection):
        username = self._get_validated_username(connection)
        cl_manager = ClientManager(self, connection, username)
        self._client_server_connections[cl_manager.get_username()] = cl_manager
        return cl_manager

    def _get_validated_username(self, connection: ClientConnection) -> str:
        connection.send_to_client(
            "Please, enter you username otherwise you can't access this server"
        )
        username = connection.receive_from_client()

        if not username:
            connection.send_to_client("Sorry, you haven't entered a proper username.")
            connection.close_client_connection()
            return

        elif username in self._client_server_connections:
            connection.send_to_client("Sorry, this username is not available")
            connection.close_client_connection()
            return

        return username


    ###### HELPER METHODS ######
    def get_connections(self):
        return self._client_server_connections

    def handle_connect(self, src_manager: ClientManager, target_username: str):
        if target_username not in self._client_server_connections:
            src_manager.send_message(f"User '{target_username}' doesn't exist")
            return

        if target_username == src_manager.get_username():
            src_manager.send_message("You cannot connect with yourself...")
            return

        target_manager = self._client_server_connections[target_username]
        session = SessionManager(src_manager, target_manager, self)
        session.create_and_handle_client_to_client_communication()

    def handle_change_username(
        self,
        requester: ClientManager,
        old_username: str,
        new_username: str,
    ):
        # only allow client_manager to access this method
        if not isinstance(requester, ClientManager):
            print("You are not a client manager, nothing is changed.")
            return

        if new_username in self._client_server_connections:
            requester.send_message(
                "You cannot choose a name of an existing user, please try another one"
            )
            return

        self._client_server_connections[new_username] = self._client_server_connections[
            old_username
        ]
        del self._client_server_connections[old_username]

        requester.send_message(
            f"Your username has been updated, your new username is {new_username}\n"
        )

        return new_username

    def handle_disconnect_client(self, username: str):
        cl_manager = self._client_server_connections[username]
        cl_manager.disconnect_client()
        del self._client_server_connections[username]
        return

    def get_connected_clients_info(self):
        pass
