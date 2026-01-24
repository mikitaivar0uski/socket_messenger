from client.client_manager import ClientManager
from client.client_states import ClientStates

class CommandHandler():
    def __init__(self):
        pass
    
    def dispatch(self, cl_manager: ClientManager, raw_input: str): # dispatch by client state
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
    
    def _handle_menu_state(self):
        pass
    
    def _handle_commands_with_args(self): # commands with args
        pass

    def _handle_commands_without_args(self):
        pass

    def _handle_chat_state(self):
        pass

    def _dispatch_chosen_option(self, 
                                client_manager: ClientManager,
                                chosen_option: str
    ):
        chosen_option = chosen_option.strip()
        print(f"chosen option is chosen {chosen_option}")
        if (
            client_manager.get_state() == self._all_states.CHAT
        ):
            print("entered chat")
            self._client_server_connections[
                client_manager.get_username()
            ].get_session().start_talking(
                self, chosen_option
            )  # refer to already created session by another user who initiated the chat

        elif client_manager.get_state() == self._all_states.MENU:
            print("entered menu")

            for option, (handler, is_special, *_) in self._all_options.items():
                if is_special and chosen_option.startswith(f"{option} "):

                    # check if only one arg was provided
                    parts = chosen_option.split()
                    option_argument = parts[1]
                    if len(parts) != 2:
                        client_manager.send_message(
                            "Correct usage: <command> <argument>. Please try again, choose one of the following: "
                        )
                        client_manager.show_menu(self._all_options)
                        return

                    # handle 'connect' option
                    if chosen_option.startswith("connect "):
                        # check if user exists
                        if option_argument not in self._client_server_connections.keys():
                            client_manager.send_message(f"User '{option_argument}' doesn't exist")
                            return

                        # disallow self connect
                        if option_argument == client_manager.get_username():
                            client_manager.send_message("You cannot connect with yourself...")
                            return
                        
                        new_ses_manager = SessionManager(
                            client_managerSrc=client_manager,
                            client_managerTarget=self._client_server_connections[option_argument],
                            smanager=self,
                        )
                        handler(new_ses_manager)
                        return

                    print(f"BUG - parts: {parts}")
                    handler(client_manager, option_argument)
                    return

                elif not is_special and chosen_option == option:
                    print(f"handler for {chosen_option} is reached")
                    handler(client_manager)
                    return

            print("skipped the loop")
            client_manager.send_message("Not a valid option, please try again: \n")
            return
        

    def set_username(
        self,
        requester: client.ClientManager,
        old_username: str,
        new_username: str,
    ):
        # only allow client_manager to access this method
        if not isinstance(requester, client.ClientManager):
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

    def handle_disconnect_client(self, requester: client.ClientManager, username: str):
        if not isinstance(requester, client.ClientManager):
            print("You are not a client manager, nothing is changed.")
            return

        del self._client_server_connections[username]
        return
    
    def handle_menu(self):
        options = self._smanager.get_all_options()

        # create menu
        message = "\nHere are all available commmands: \n"
        for option, (*_, option_description) in options.items():
            message += f"\t- {option + option_description}\n"

        self.send_message(message)
        return

    def handle_show_available_clients(self):
        connections = self._smanager.get_connections()

        lines = []

        for username, client_manager in connections.items():
            if username == self.get_username():
                continue
            
            match client_manager.get_state():
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
            self.send_message("There are no other users connected...")
            return
        
        message = "\n".join(lines)

        self.send_message(message)
        return