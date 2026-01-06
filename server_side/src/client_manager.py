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
        self._username = username
        self._client_socket = client_socket
        self._addr = addr
        self._state: ClientStates = state

        self._smanager = smanager
        self._ses_manager: "ses_manager" = None

    def send_message(self, message: str):
        self._client_socket.send(message.encode())
        return

    def send_message_include_sender(self, message: str, sender: str):
        message = f"{sender}: {message}"
        self._client_socket.send(message.encode())
        return

    def receive_message(self):
        message = self._client_socket.recv(1024).decode()
        return message

    def show_menu(self, options: dict = None):
        if not options:
            options = self._smanager.get_all_options()

        # create a menu
        message = "\nHere are all available commmands: \n"
        for option, (*_, option_description) in options.items():
            message += f"\t- {option + option_description}\n"

        self.send_message(message)
        return

    def show_available_clients(self):
        connections = self._smanager.get_connections()

        lines = []

        for username, cmanager in connections.items():
            if username == self.get_username():
                continue
            
            match cmanager.get_state():
                case ClientStates.CHAT:
                    status =  " (unavailable)"
                case  ClientStates.MENU:
                    status = ""
                case ClientStates.DISCONNECTED:
                    status = " (disconnected)"
                case _:
                    status = " (unknown status, please contact support)"

            lines.append(f"- {username}{status}")

        if not lines:
            self.send_message("No other users connected...")
            return
        
        message = "\n".join(lines)

        self.send_message(message)
        return

    def disconnect_client(self):
        self._client_socket.close()
        self._state = ClientStates.DISCONNECTED
        return self._smanager.disconnect_client(self, self._username)

    def set_username(self, new_username: str):
        if new_username == self.get_username():
            self.send_message("What's the point of changing your username if it's the same as before?..")
            return
        
        old_username = self._username

        # update name server wide
        if not self._smanager.set_username(
            self, old_username=old_username, new_username=new_username
        ):
            return
        
        self._username = new_username
        return

    def set_state(self, new_state: ClientStates):
        if not isinstance(new_state, ClientStates):
            print(
                "[ERROR] - the state isn't changed, not a member of enum - ClientState"
            )
            return
        self._state = new_state
        return

    def set_session(self, session: "ses_manager"):
        self._ses_manager = session
        return

    def get_username(self):
        return self._username

    def get_state(self):
        return self._state

    def get_session(self):
        return self._ses_manager
