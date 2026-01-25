# core functionality
import socket
import threading

# config
from dotenv import load_dotenv
import os

# typehinting
from typing import Callable

# internal modules
import server_side.src.core.client.client_manager as client_manager
from server_side.src.core.server.session_manager import SessionManager
from server_side.src.core.client.client_states import ClientStates
from client.client_manager import ClientManager

from network.server_listener import Listener
from network.client_connection import ClientConnection

load_dotenv()


class ServerManager:
    def __init__(
        self,
        server_ip: str = os.getenv("LISTENING_ADDRESS"),
        server_port: int = int(os.getenv("LISTENING_PORT")),
    ):

        self._server_ip = server_ip
        self._server_port = server_port
        self._listening_socket: socket.socket = None
        self._client_server_connections: dict[str, client_manager.ClientManager] = {}

        self._all_options = all_options
        self._all_states: ClientStates = ClientStates

        self._all_sessions: dict[str, tuple[SessionManager, SessionManager]] = {}

    #### INIT CONNECTION ####
    def connection_setup(self):
        listener = Listener(self._server_ip, self._server_port)
        listener.start_listening()
        while listener.running:
            new_connection = listener.accept_connections()
            new_thread = threading.Thread(target=self._handle_connection, 
                                          args=(new_connection))
            new_thread.start()

    #### HANDLE CONNECTION ####
    def _handle_connection(self, connection: ClientConnection, client_addr: str):
        print(f"The type of all_states is {type(self._all_states)}")
        print(f"THREAD started for {client_addr}")

        username = self._get_verified_username(ClientConnection)
        if username is None:
            return

        self._register_client(ClientConnection, client_addr, username)

        self._client_server_connections[username].show_menu(self._all_options)

        self._serve(cmanager=self._client_server_connections[username])

    def _get_verified_username(self, client_socket: socket.socket) -> str:
        client_socket.send(
            "Please, enter you username otherwise you can't access this server".encode()
        )
        print("Waiting for username input from...")
        username = client_socket.recv(512).decode().strip()
        print(f"Username received is {username} with type: {type(username)}")

        # drop connection if no/ empty username was sent
        if not username:
            client_socket.send("Sorry, you haven't entered a proper username.".encode())
            client_socket.close()
            return None

        elif username in self._client_server_connections:
            client_socket.send("Sorry, this username is not available".encode())
            client_socket.close()
            return None

        print(f"Username {username} is accepted")
        return username

    def _register_client(self, c_socket: socket.socket, c_addr: str, c_username: str):
        new_cmanager = client_manager.ClientManager(
            smanager=self,
            client_socket=c_socket,
            addr=c_addr,
            username=c_username,
            state=self._all_states.MENU,
        )
        self._client_server_connections[c_username] = new_cmanager
        return

    def _serve(self, cmanager: client_manager.ClientManager):
        try:
            while cmanager.get_state() != self._all_states.DISCONNECTED:
                print(f"Waiting for chosen_option from {cmanager.get_username()}...")
                chosen_option = cmanager.receive_message()
                print(
                    f"Raw chosen option from user {cmanager.get_username()} is {repr(chosen_option)}, the type is {type(chosen_option)}"
                )
                self._dispatch_chosen_option(cmanager, chosen_option)
        except ConnectionResetError as cre:
            print(
                f"USER {cmanager.get_username()} forcibly closed connection. {repr(cre)}"
            )
            cmanager.disconnect_client()
            return
        except Exception as e:
            print(f"EXCEPTION is reached in handler {repr(e)}")
            cmanager.disconnect_client()
            return

    #### DISPATCH CLIENT'S INPUT ####

    def _dispatch_chosen_option(
        self, cmanager: client_manager.ClientManager, chosen_option: str
    ):
        chosen_option = chosen_option.strip()
        print(f"chosen option is chosen {chosen_option}")
        if cmanager.get_state() == self._all_states.CHAT:
            print("entered chat")
            self._client_server_connections[
                cmanager.get_username()
            ].get_session().start_talking(
                self, chosen_option
            )  # refer to already created session by another user who initiated the chat

        elif cmanager.get_state() == self._all_states.MENU:
            print("entered menu")

            for option, (handler, is_special, *_) in self._all_options.items():
                if is_special and chosen_option.startswith(f"{option} "):

                    # check if only one arg was provided
                    parts = chosen_option.split()
                    option_argument = parts[1]
                    if len(parts) != 2:
                        cmanager.send_message(
                            "Correct usage: <command> <argument>. Please try again, choose one of the following: "
                        )
                        cmanager.show_menu(self._all_options)
                        return

                    # handle 'connect' option
                    if chosen_option.startswith("connect "):
                        # check if user exists
                        if (
                            option_argument
                            not in self._client_server_connections.keys()
                        ):
                            cmanager.send_message(
                                f"User '{option_argument}' doesn't exist"
                            )
                            return

                        # disallow self connect
                        if option_argument == cmanager.get_username():
                            cmanager.send_message("You cannot connect with yourself...")
                            return

                        new_ses_manager = SessionManager(
                            cmanagerSrc=cmanager,
                            cmanagerTarget=self._client_server_connections[
                                option_argument
                            ],
                            smanager=self,
                        )
                        handler(new_ses_manager)
                        return

                    print(f"BUG - parts: {parts}")
                    handler(cmanager, option_argument)
                    return

                elif not is_special and chosen_option == option:
                    print(f"handler for {chosen_option} is reached")
                    handler(cmanager)
                    return

            print("skipped the loop")
            cmanager.send_message("Not a valid option, please try again: \n")
            return

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
        requester: client_manager.ClientManager,
        old_username: str,
        new_username: str,
    ):
        # only allow client_manager to access this method
        if not isinstance(requester, client_manager.ClientManager):
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

    def get_all_options(self):
        return self._all_options

    def get_connected_clients_info(self):
        pass
