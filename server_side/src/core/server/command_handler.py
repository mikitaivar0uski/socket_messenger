from typing import Callable, TYPE_CHECKING
from core.client.client_states import ClientStates

class ParsedCommand():
    def __init__(self, handler: Callable, command: str, argument: str|None = None):
        self.command: str
        self.argument: str|None = argument
        self.handler: Callable = handler

class CommandHandler():
    def __init__(self, smanager: "ServerManager"):
        self.smanager = smanager
        self._commands: dict[str, tuple[Callable, bool, str]] = {
            "ls": (self.handle_ls, False, " - list all users except you"),
            "disconnect": (self.handle_disconnect, False, " - disconnect from server"),
            "connect": (
                self.handle_connect,
                True,
                " <target_username> - enter chat with another user if available"
            ),
            "username": (self.handle_change_username, True, " <new_username> - change your username"),
            "menu": (self.handle_display_menu, False, " - display all options again"),
        }


### VALIDATE & DISPATCH LOGIC ###
    def dispatch(self, cl_manager: "ClientManager", raw_input: str): # dispatch by client state
        raw_input = raw_input.strip()

        if not raw_input:
            return
        
        match cl_manager.get_state():
            case ClientStates.CHAT:
                self._handle_chat_state(cl_manager, raw_input)
            case ClientStates.MENU:
                self._handle_menu_state(cl_manager, raw_input)
            case _:
                cl_manager.send_message("Invalid client state.")
    
    def _handle_menu_state(self, client_manager: "ClientManager", raw_input: str):
        parsed_command = self._parse_menu_command(client_manager, raw_input)
        if parsed_command:
            if parsed_command.argument:
                parsed_command.handler(client_manager, parsed_command.argument)
                return
            parsed_command.handler(client_manager)
            return
    
    def _parse_menu_command(self, client_manager: "ClientManager", raw_input: str):
        parts = raw_input.split()

        if len(parts) > 2:
            client_manager.send_message("Commands can't have more than 1 argument")
            return
        
        command = parts[0]
        if command not in self._commands:
            client_manager.send_message(f"Command {command} doesn't exist")
            return
        
        handler = self._get_handler(command)
        if len(parts) == 2:
            argument = parts[1]
            if not argument:
                client_manager.send_message("Argument can't be empty")
                return
            parsed_command = ParsedCommand(handler, command, argument)
            
        elif len(parts) == 1:
            parsed_command = ParsedCommand(handler, command)

        return parsed_command


    def _handle_chat_state(self, client_manager: "ClientManager", raw_input: str):
        client_manager.get_session().start_talking(
            self, raw_input
        )  # refer to already created session by another user who initiated the chat


### HANDLERS (SPECIAL)###
    def handle_connect(self, cl_manager: "ClientManager", target_username: str):
        self.smanager.handle_connect(cl_manager, target_username)

    def handle_change_username(self, cl_manager: "ClientManager", new_username: str):
        self.smanager.handle_change_username(cl_manager, new_username)


### HANDLERS (NOT SPECIAL)###
    def handle_ls(self, client_manager: "ClientManager"):
        info = self.smanager.get_connected_clients_states()

        lines = []

        for username, state in info.items():
            if username == client_manager.get_username():
                continue
            
            match state:
                case ClientStates.CHAT:
                    status =  "(unavailable)"
                case  ClientStates.MENU:
                    status = ""
                case ClientStates.DISCONNECTED:
                    status = "(disconnected)"
                case _:
                    status = "(unknown status)"

            lines.append(f"\t- {username} {status}")

        if not lines:
            client_manager.send_message("There are no other users connected...")
            return
        
        message = "\n".join(lines)

        client_manager.send_message(message)
        return

    def handle_disconnect(self, cl_manager: "ClientManager"):
        self.smanager.handle_disconnect_client(cl_manager)

    def handle_display_menu(self, cl_manager: "ClientManager"):
        # create menu
        menu = "\nHere are all available commmands: \n"
        for command, (*_, command_description) in self._commands.items():
            menu += f"\t- {command + command_description}\n"

        cl_manager.send_message(menu)
        return
    
    def _get_handler(self, command: str) -> Callable:
        return self._commands[command][0]