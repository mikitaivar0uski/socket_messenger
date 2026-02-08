import unittest
from unittest.mock import Mock

from socket_messenger.core.server.command_handler import CommandHandler
from socket_messenger.core.client.client_states import ClientStates

class TestCommandHandler(unittest.TestCase):
    def setUp(self):
        self.client_states = ClientStates
        self._smanager = Mock()
        self.cl_manager = Mock()
        self.cl_manager.get_username.return_value = "yehor"

        self.command_handler = CommandHandler(self._smanager)

### ls handler ###
    def test_ls_no_other_users(self):
        self._smanager.get_connected_clients_states.return_value = {
            "yehor": self.client_states.MENU
        }

        self.command_handler.handle_ls(self.cl_manager)

        self.cl_manager.send_message.assert_called_once_with(
            "There are no other users connected..."
        )


    def test_ls_one_another_user(self):
        self._smanager.get_connected_clients_states.return_value = {
            "yehor": self.client_states.MENU,
            "bob": self.client_states.MENU
        }

        self.command_handler.handle_ls(self.cl_manager)

        self.cl_manager.send_message.assert_called_once_with(
            "\t- bob "
        )


### menu handler ###
    def test_display_menu(self):
        self.command_handler.handle_display_menu(self.cl_manager)
        expected = (
        "\nHere are all available commmands: \n"
        "\t- ls - list all users except you\n"
        "\t- disconnect - disconnect from server\n"
        "\t- connect <target_username> - enter chat with another user if available\n"
        "\t- username <new_username> - change your username\n"
        "\t- menu - display all options again\n"
        )

        self.cl_manager.send_message.assert_called_once_with(expected)


if __name__ == "__main__":
    unittest.main()