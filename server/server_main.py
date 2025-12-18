import socket
import threading
from typing import Callable

import client_manager, server_manager


def main():
    smanager = server_manager.smanager()
    # create a listening_socket and listen for new connections
    smanager.create_listening_socket()
    # accept new connections for clients who entered username, constantly updates 'connections', state = "menu"
    # performs: while True: accept | create connection | display menu
    smanager.create_client_server_connections()

    # smanager.dispatch_chosen_option()


if __name__ == "__main__":
    main()


# open a port
# listen for connections
# bind a connection to a new socket that exists in a new thread
# create a tuple with two sockets - two clients -> if client sends data - send it to another client
# never close a port
