import server_side.src.core.server.server_manager as server_manager


def main():
    serv_manager = server_manager.ServerManager()
    # create a listening_socket and listen for new connections
    serv_manager.listen_for_new_connections()
    # accept new connections for clients who entered username, create a thread for each one and handle each connection
    serv_manager.accept_and_handle_incoming_connections()


if __name__ == "__main__":
    main()


