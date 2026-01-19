import threading
import os
from dotenv import load_dotenv

from network import Network
from core import Core
from ui import UI

load_dotenv()

def user_input_loop(core):
    while core.running:
        try:
            message = core.ui.read()
            if not core.running:
                break
            core.on_user_input(message)
        except (EOFError, KeyboardInterrupt):
            core.stop()

def server_receive_loop(core):
    while core.running:
        try:
            message = core.network.receive_from_server()
            core.on_server_message(message)
        except Exception as e:
            core.stop()

def main():
    network_manager = Network(os.getenv("SERVER_ADDRESS"), int(os.getenv("SERVER_PORT")))
    ui_manager = UI()
    core = Core(network_manager, ui_manager)
    network_manager.connect_to_server()
    input_thread = threading.Thread(
        target=user_input_loop,
        args=([core])
    )
    server_thread = threading.Thread(
        target=server_receive_loop,
        args=([core])
    )
    input_thread.start()
    server_thread.start()
    input_thread.join()
    server_thread.join()

if __name__ == "__main__":
    main()
