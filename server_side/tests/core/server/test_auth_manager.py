import unittest
from unittest.mock import MagicMock

from core.server.auth_manager import AuthManager

class TestPasswordValidation(unittest.TestCase):

    def setUp(self):
        self.auth = AuthManager(
            connection=MagicMock(),
            storage=MagicMock()
        )

    def test_valid_password(self):
        success, msg = self.auth._validate_password_format("ab12c")
        self.assertTrue(success)
        self.assertEqual(msg, "")

    def test_too_short_password(self):
        success, msg = self.auth._validate_password_format("a1b")
        self.assertFalse(success)
        self.assertIn("too short", msg)

    def test_not_enough_digits(self):
        success, msg = self.auth._validate_password_format("abcde")
        self.assertFalse(success)
        self.assertIn("numbers", msg)

    def test_not_enough_letters(self):
        success, msg = self.auth._validate_password_format("12345")
        self.assertFalse(success)
        self.assertIn("letters", msg)

    def test_password_with_spaces(self):
        success, msg = self.auth._validate_password_format("ab 12")
        self.assertFalse(success)

    def test_password_too_long(self):
        success, msg = self.auth._validate_password_format("ab12ab12ab12ab12ab12ab12ab12ab12")
        self.assertFalse(success)


class TestLogin(unittest.TestCase):

    def setUp(self):
        self.connection = MagicMock()
        self.storage = MagicMock()
        self.auth = AuthManager(self.connection, self.storage)

    def test_login_success(self):
        # simulate user input
        self.connection.receive_from_client.side_effect = [
            "john",      # username
            "ab12cd"     # password
        ]

        self.storage.client_exists.return_value = True
        self.storage.verify_password.return_value = True

        username, msg = self.auth.login()

        self.assertEqual(username, "john")
        self.assertEqual(msg, "")


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.connection = MagicMock()
        self.storage = MagicMock()
        self.auth = AuthManager(self.connection, self.storage)

    def test_register_username_taken(self):
        self.connection.receive_from_client.return_value = "john"
        self.storage.client_exists.return_value = True

        username, msg = self.auth.register()

        self.assertEqual(username, "")
        self.assertIn("not available", msg)


if __name__ == "__main__":
    unittest.main()