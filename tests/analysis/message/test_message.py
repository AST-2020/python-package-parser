import unittest
from unittest import TestCase

from analysis.message import Message


class TestMessage(TestCase):
    def test_str(self):
        expected = "Error in 'File' line 2: Description"
        actual = str(Message("File", 2, "Description"))

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
