from storage.storage_manager import StorageManager
from network.client_connection import ClientConnection

class AuthManager:
    def __init__(self, connection: ClientConnection, storage: StorageManager):
        self._connection = connection
        self._storage = storage

    def authenticate_client(self) -> str:
        while True:
            self._connection.send_to_client("Would you like to /login or /register ?")
            command = self._connection.receive_from_client().strip()

            if not command:
                self._connection.send_to_client(
                    "Seems like you didn't enter anything, please try again"
                )
                continue
            elif len(command.split()) != 1:
                self._connection.send_to_client(
                    "Too many arguments, should be either '/login' or '/register', nothing more... Please try again"
                )
                continue
            elif command == "/login":
                username, description = self.login()
                if not username:
                    self._connection.send_to_client(description)
                    continue
                break
            elif command == "/register":
                username, description = self.register()
                if not username:
                    self._connection.send_to_client(description)
                    continue
                break
            else:
                self._connection.send_to_client("Yeah, idk what happened... Please try again")

        return username


    def login(self) -> tuple[str, str]:
        username, description = self._get_validated_username(must_exist=True)
        if not username:
            return "", description
        
        password, description = self._prompt_for_password()
        if not self._storage.verify_password(username, password):
            description = "Password is not correct"
            return "", description
        
        return username, ""

    def register(self) -> tuple[str, str]:
        username, description = self._get_validated_username(must_exist=False)
        if not username:
            return "", description

        password, description = self._prompt_for_password()
        if not password:
            return "", description

        # Add client to persistent storage
        success = self._storage.create_client(username, password)
        if not success:
            description = "Couldn't add information to our storage..."
            return "", description

        return username, ""

    def _get_validated_username(
        self, must_exist: bool
    ) -> tuple[str, str]:
        """
        Requests a username from the client and validates it
        """
        self._connection.send_to_client("Please, enter username")
        username = self._connection.receive_from_client()

        if not username:
            description = (
                "Sorry, you haven't entered a proper username"
            )
            return "", description

        if not must_exist:
            if self._storage.client_exists(username):
                description = (
                    "Sorry, this username is not available"
                )
                return "", description

        return username, ""

    def _prompt_for_password(self) -> tuple[str, str]:
        self._connection.send_to_client(
            "Please, enter password (at least 2 letters and 2 numbers, at least 5 characters long, max - 15 characters))"
        )
        password = self._connection.receive_from_client()
        success, descripton = self._validate_password_format(password)
        if not success:
            return "", descripton
        return password, ""

    def _validate_password_format(self, password: str) -> tuple[bool, str]:
        """
        Split into validate password and get_password loop?? to allow for easy unit tests and make it more transparent
        Return a tuple Boolean-Description: str
        learn to use letters/ digits with list comprehensions
        """

        if len(password.split()) > 1:
            description = "Password should be one continuous string, no white spaces"
            return  False, description

        if len(password) > 15:
            description = "Your password is too long"
            return  False, description

        if len(password) < 5:
            description = "Your password is too short"
            return  False, description

        digits = sum(i.isdigit() for i in password)
        letters = sum(i.isalpha() for i in password)

        if digits < 2:
            description = "Password must contain at least 2 numbers"
            return  False, description

        if letters < 2:
            description = "Password must contain at least 2 letters"
            return  False, description

        return True, ""