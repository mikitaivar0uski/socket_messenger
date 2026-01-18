from abc import ABC, abstractmethod


class NetworkHandler(ABC):

    @abstractmethod
    def connect_to_server(self):
        pass

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self):
        pass

    @abstractmethod
    def disconnect_from_server(self):
        pass
