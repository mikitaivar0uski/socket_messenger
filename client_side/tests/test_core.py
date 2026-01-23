import sys
sys.path.insert(0, "C:\\Users\\YehorSolonukha\\My_Career\DevOps\\05_Python\\communicator\\client-server\\main\\client_side\\src")

import unittest
from unittest.mock import Mock
from core import Core


class TestCore(unittest.TestCase):

    def setUp(self):
        self.mock_network = Mock()
        self.mock_ui = Mock()
        self.core = Core(self.mock_network, self.mock_ui)

    def test_on_user_input_send_message_when_running(self):
        self.core.running = True
        message = "Hello"
        self.core.on_user_input(message)
        self.mock_network.send_to_server.assert_called_once_with(message)

    def test_on_user_input_doesnt_send_message_when_not_running(self):
        self.core.running = False
        message = "Hello"
        self.core.on_user_input(message)
        self.mock_network.send_to_server.assert_not_called()

if __name__ == "__main__":
    unittest.main()