from client_manager import cmanager
from server_manager import smanager
from client_states import ClientState


class ses_manager():
    def __init__(self, cmanagerSrc: cmanager, cmanagerTarget: cmanager, smanager: smanager):
        self.cmanagerSrc = cmanagerSrc
        self.cmanagerTarget = cmanagerTarget
        self.smanager = smanager


    def create_client_client_connections(self):
        # get message from client x send to client y | another thread repeats...
        if not self._target_available():
            self.cmanagerSrc.send(f"Unable to connect with {self.cmanagerTarget.getName()}, user is in 'chat' mode... \n Please try again later")
            return

        elif self._target_available():
            self.cmanagerSrc.change_state(ClientState.CHAT)
            self.cmanagerTarget.change_state(ClientState.CHAT)
            while True:
                message = self.cmanagerSrc.receive()

                if message=='/exit':
                    message=f"{cmanager.getName()} decided to exit the chat"
                    self.cmanagerTarget.send_named(message, self.cmanagerSrc.getName())
                    self.cmanagerTarget.disconnect_client()
                    self.cmanagerSrc.disconnect_client()
                    return
                
                self.cmanagerTarget.send_named(message, self.cmanagerSrc.getName())

    
    def _target_available(self):
        if self.cmanagerTarget.getState() == ClientState.CHAT:
            return False
        elif self.cmanagerTarget.getState() == ClientState.MENU:
            return True