import unittest

from random import choice
from string import ascii_letters

from main import OrderHandler as Order


class UserTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.test_string = ''.join(choice(ascii_letters) for i in range(70))
        print(self.test_string)

    def test_rename_task_title(self):
        expected_value = f'{self.test_string[:50]}...'
        print(expected_value)
        self.assertEqual(
            Order.rename_task_title(self.test_string),
            expected_value
        )
