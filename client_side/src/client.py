# core functionality
import socket
import threading

# config
from dotenv import load_dotenv
import os

load_dotenv()

class Client:
    def __init__(self, server_address: str = os.getenv("SERVER_ADDRESS"), server_port: int = int(os.getenv("SERVER_PORT"))):
        self.socket = None
        self.server_address = server_address
        self.server_port = server_port

    def establish_connection(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_address, self.server_port))
        return

    def receive_the_menu(self):
        menu = self.__receive()
        print(menu)
        return

    def talk_to_server(self):
        t1 = threading.Thread(target=self.__listen_for_input_and_send)
        t2 = threading.Thread(target=self.__listen_to_server_and_display)
        t1.start()
        t2.start()
        try:
            t1.join()
            t2.join()
        except KeyboardInterrupt as ki:
            print(f"EXCEPTION {repr(ki)}")
            self.socket.close()

    def __listen_for_input_and_send(self):
        while True:
            try:
                message = input()
                if not message:
                    continue
                self.__send(message)
            except (EOFError, KeyboardInterrupt):
                self.socket.close()
                break
            except Exception as e:
                self.socket.close()
                print("EXCEPTION raised: " + repr(e))
                break

    def __listen_to_server_and_display(self):
        while True:
            try:
                response = self.__receive()
                if not response:
                    print("Server disconnected.")
                    break
                print(response)
            except ConnectionAbortedError:
                print("Server disconnected.")
                break
            except Exception as e:
                print("EXCEPTION from server: " + e)
                break

    def __receive(self):
        response = self.socket.recv(1024).decode()
        return response

    def __send(self, message: str):
        self.socket.send(message.encode())
        return
