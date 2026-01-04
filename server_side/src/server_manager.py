# core functionality
import socket
import threading

# config
from dotenv import load_dotenv
import os

# typehinting
from typing import Callable

# internal modules
import client_manager
from session_manager import SessionManager
from client_states import ClientStates

load_dotenv()

class ServerManager:
    def __init__(
        self,
        listening_addr: str = os.getenv("LISTENING_ADDRESS"),
        listening_port: int = int(os.getenv("LISTENING_PORT")),
        all_options: dict[str, tuple[Callable, bool, str]] = {
            "ls": (client_manager.ClientManager.show_available_clients, False, " - list all users except you"),
            "disconnect": (client_manager.ClientManager.disconnect_client, False, " - disconnect from server"),
            "connect": (
                SessionManager.create_and_handle_client_to_client_communication,
                True,
                " <target_username> - enter chat with another user if available"
            ),
            "username": (client_manager.ClientManager.set_username, True, " <new_username> - change your username"),
            "menu": (client_manager.ClientManager.show_menu, False, " - display all options again"),
        },
    ):

        self._listening_address = listening_addr
        self._listening_port = listening_port
        self._listening_socket: socket.socket = None
        self._client_server_connections: dict[str, client_manager.ClientManager] = {}

        self._all_options = all_options
        self._all_states: ClientStates = ClientStates

        self._all_sessions: dict[str, tuple[SessionManager, SessionManager]] = {}

### INITIATE CONNECTION WITH THE SERVER ###

    def listen_for_new_connections(self):
        self._listening_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )  # ipv4 + tcp
        print(self._listening_address)
        print(self._listening_port)
        server_address = (self._listening_address, self._listening_port)
        self._listening_socket.bind(server_address)
        self._listening_socket.listen(20)

        return

    def accept_and_handle_incoming_connections(self):
        # accept client_server_connections
        while True:
            print("Waiting for new connections...")
            client_socket, client_addr = self._listening_socket.accept()
            print(f"Incoming connection from {client_addr}")

            client_thread = threading.Thread(
                target=self._handle_connection,
                args=(client_socket, client_addr),
            )
            client_thread.daemon = True
            client_thread.start()

### HANDLE CONNECTION ###

    def _handle_connection(self, client_socket: socket.socket, client_addr: str):
        print(f"The type of all_states is {type(self._all_states)}")
        print(f"THREAD started for {client_addr}")

        username = self._get_verified_username(client_socket)
        if username is None:
            return
        
        self._register_client(client_socket, client_addr, username)

        self._client_server_connections[username].show_menu(self._all_options)

        self._serve(cmanager=self._client_server_connections[username])


    def _get_verified_username(self, client_socket: socket.socket) -> str:
        client_socket.send(
            "Please, enter you username otherwise you can't access this server".encode()
        )
        print("Waiting for username input from...")
        username = client_socket.recv(512).decode().strip()
        print(f"Username received is {username} with type: {type(username)}")

        # drop connection if no username was entered
        if not username:
            client_socket.send("Sorry, you haven't entered a proper username.".encode())
            client_socket.close()
            return None

        elif username in self._client_server_connections:
            client_socket.send(
                "Sorry, this username is not available".encode()
            )
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
            print(f"USER {cmanager.get_username()} forcibly closed connection. {repr(cre)}")
            cmanager.disconnect_client()
            return
        except Exception as e:
            print(f"EXCEPTION is reached in handler {repr(e)}")
            cmanager.disconnect_client()
            return

### DISPATCH CLIENT'S INPUT ###

    def _dispatch_chosen_option(
        self, cmanager: client_manager.ClientManager, chosen_option: str
    ):
        chosen_option = chosen_option.strip()
        print(f"chosen option is chosen {chosen_option}")
        if (
            cmanager.get_state() == self._all_states.CHAT
        ):  # define missing methods and properties\
            print("entered chat")
            self._client_server_connections[
                cmanager.get_username()
            ].get_session().start_talking(
                self, chosen_option
            )  # refer to already created session by another user

        elif cmanager.get_state() == self._all_states.MENU:
            print("entered menu")
            # check if chosen_option is available
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

                    # handler for connect
                    if chosen_option.startswith("connect "):
                        # check if user exists
                        if option_argument not in self._client_server_connections.keys():
                            cmanager.send_message(f"User '{option_argument}' doesn't exist")
                            return

                        # disallow self connect
                        if option_argument == cmanager.get_username():
                            cmanager.send_message("You cannot connect with yourself...")
                            return
                        
                        new_ses_manager = SessionManager(
                            cmanagerSrc=cmanager,
                            cmanagerTarget=self._client_server_connections[option_argument],
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

    ###### HELPER METHODS FOR CLIENT MANAGER ######

    def set_username(
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
            requester.send_message("You cannot choose a name of an existing user, please try another one")
            return

        self._client_server_connections[new_username] = (
            self._client_server_connections[old_username]
        )
        del self._client_server_connections[old_username]

        requester.send_message(
            f"Your username has been updated, your new username is {new_username}\n"
        )

        return new_username

    def disconnect_client(self, requester: client_manager.ClientManager, username: str):
        if not isinstance(requester, client_manager.ClientManager):
            print("You are not a client manager, nothing is changed.")
            return

        del self._client_server_connections[username]
        return

    def get_all_options(self):
        return self._all_options


###### HELPER METHODS FOR SESSION MANAGER ######

# def update_sessions(self, src_name: str, src_ses_manager: ses_manager, tgt_ses_manager: ses_manager):
#    self.__all_sessions[src_name]=(src_ses_manager, tgt_ses_manager)
#    return
