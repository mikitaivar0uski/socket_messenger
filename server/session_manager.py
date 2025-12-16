from client_manager import cmanager
from client_states import ClientState


class ses_manager():
    def __init__(self, cmanagerSrc: cmanager, cmanagerTarget: cmanager, smanager: "smanager"):
        self.cmanagerSrc = cmanagerSrc
        self.cmanagerTarget = cmanagerTarget
        self.smanager = smanager


    def create_client_client_connections(self):
        # check if target exist
        if not self.__check_if_target_exists():
            self.cmanagerSrc.send("Target doesn't exist in our data base, please try again later")
            return
        
        # check if target available
        if not self.__check_if_target_available():
            self.cmanagerSrc.send(f"Unable to connect with {self.cmanagerTarget.getName()}, user is in 'chat' mode... \n Please try again later")
            return
        

        # set sessions for both
        self.__set_sessions_in_cmanagers()
        # change states for both
        self.__change_states_to_chat()
        
        #self.__set_sessions_in_global_dictionary()

        # notify target that it is chatting with source (probably not needed)
        # self.cmanagerTarget.send(f"You are now in chat with {self.cmanagerSrc.getName()}")

        # relay messages from source to target
        self.__announce_established_connection_to_both_clients()
        self.initialize_communication(requester=self)

        return
    


    def initialize_communication(self, requester, message: str = None):
        # check if requester is smanager or self
        #if not (isinstance(requester, 'smanager') or isinstance(requester, self)):
        #    print("Not autorized to use this method - 'initialize_communication()'")
        #    return

        if not message:
            message = self.cmanagerSrc.receive()

        while True:
            if message=='/exit':
                self.__handle_exit_message()
                return
            
            self.cmanagerTarget.send_named(message, self.cmanagerSrc.getName())
            message = self.cmanagerSrc.receive()
          
          
    def __handle_exit_message(self):
        # change each client's session to None
        self.__set_sessions_in_cmanagers_to_None()

        # change each client's state back to MENU
        self.__change_states_to_menu()

        # send (chat ended)
        self.cmanagerSrc.send(f"You exited the chat with {self.cmanagerTarget.getName()}.")

        self.cmanagerTarget.send(f"{self.cmanagerSrc.getName()} decided to exit the chat.")
        return
    
    def __announce_established_connection_to_both_clients(self):
        self.cmanagerSrc.send(f"You entered a chat with {self.cmanagerTarget.getName()}, please type /exit to exit.\n")
        self.cmanagerTarget.send(f"You entered a chat with {self.cmanagerSrc.getName()}, please type /exit to exit.\n")
        return
    
    
    def __set_sessions_in_cmanagers(self):
        self.cmanagerSrc.change_session(self)

        target_session = ses_manager(self.cmanagerTarget, self.cmanagerSrc, self.smanager)
        self.cmanagerTarget.change_session(target_session)
        return 
    
    def __set_sessions_in_cmanagers_to_None(self):
        self.cmanagerSrc.change_session_to_None()
        self.cmanagerTarget.change_session_to_None()
    #def __set_sessions_in_global_dictionary(self):
    #    target_session = ses_manager(self.cmanagerTarget, self.cmanagerSrc, self.smanager)
    #
    #    self.smanager.update_sessions(self.cmanagerSrc.getName(), self, target_session)
    #    self.smanager.update_sessions(self.cmanagerTarget.getName(), target_session, self)
    #    return



    def __check_if_target_exists(self):
        if self.smanager.getConnections()[self.cmanagerTarget.getName()]:
            return True
        return False
    


    def __check_if_target_available(self):
        if self.cmanagerTarget.getState() == ClientState.MENU:
            return True
        elif self.cmanagerTarget.getState() == ClientState.CHAT:
            return False
        self.cmanagerSrc("Unknown error occured, please wait until we resolve it")
        print("New ClientState.STATE isn't handled")
        return


    

    def __change_states_to_chat(self):
        self.cmanagerSrc.change_state(ClientState.CHAT)
        self.cmanagerTarget.change_state(ClientState.CHAT)
        return
    

    def __change_states_to_menu(self):
        self.cmanagerSrc.change_state(ClientState.MENU)
        self.cmanagerTarget.change_state(ClientState.MENU)
        return
