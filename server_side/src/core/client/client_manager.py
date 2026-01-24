from server_side.src.core.client.client_states import ClientStates
from server_side.src.network.client_connection import ClientNetwork


class ClientManager:
    def __init__(
        self,
        smanager: "server_manager.ServerManager",
        connection: ClientNetwork,
        username: str,
        state: ClientStates,
    ):
        self._username = username
        self.connection: ClientNetwork = connection
        self._state: ClientStates = state

        self._smanager = smanager
        self._ses_manager: "ses_manager" = None

# basic IO
    def send_message(self, message: str):
        self.connection.send_to_client(message)
        return

    def send_message_include_sender(self, message: str, sender: str):
        message = f"{sender}: {message}"
        self.connection.send_to_client(message)
        return

    def receive_message(self):
        message = self.connection.receive_from_client()
        return message

# session management
    def disconnect_client(self):
        self.connection.close_client_connection()
        self.set_state(ClientStates.DISCONNECTED)
        return self._smanager.disconnect_client(self, self._username)

# getter/ setters
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
