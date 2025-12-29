import socket
from client_states import ClientStates


class ClientManager:
    def __init__(
        self,
        smanager: "server_manager.ServerManager",
        client_socket: socket.socket,
        addr: str,
        username: str,
        state: ClientStates,
    ):
        self.__username = username
        self.__client_socket = client_socket
        self.__addr = addr
        self.__state: ClientStates = state

        self.__smanager = smanager
        self.__ses_manager: "ses_manager" = None

    def send_message(self, message: str):
        self.__client_socket.send(message.encode())
        return

    def send_message_include_sender(self, message: str, sender: str):
        message = f"{sender}: {message}"
        self.__client_socket.send(message.encode())
        return

    def receive_message(self):
        message = self.__client_socket.recv(1024).decode()
        return message

    def show_menu(self, options: dict = None):
        if not options:
            options = self.__smanager.get_all_options()
        # create a menu
        message = "\nHere are all available commmands: \n"
        for option, (*_, option_description) in options.items():
            message += f"\t- {option + option_description}\n"

        # send the menu
        self.send_message(message)
        return

    def show_available_clients(self):
        connections = self.__smanager.get_connections().keys()
        print(f"Connections are {connections}")
        client_names = list(connections)
        client_names.remove(self.get_username())
        client_names_to_send = "\n\t-".join(client_names) + "\n"

        self.send_message(client_names_to_send)
        return

    def disconnect_client(self):
        self.__client_socket.close()
        self.__state = ClientStates.DISCONNECTED
        return self.__smanager.disconnect_client(self, self.__username)

    def set_username(self, new_username: str):
        # update name in instance of this class
        old_username = self.__username
        self.__username = new_username
        # update name server wide
        return self.__smanager.set_username(
            self, old_username=old_username, new_username=new_username
        )

    def set_state(self, new_state: ClientStates):
        if not isinstance(new_state, ClientStates):
            print(
                "[ERROR] - the state isn't changed, not a member of enum - ClientState"
            )
            return
        self.__state = new_state
        return

    def set_session(self, session: "ses_manager"):
        self.__ses_manager = session
        return

    def get_username(self):
        return self.__username

    def get_state(self):
        return self.__state

    def get_session(self):
        return self.__ses_manager
