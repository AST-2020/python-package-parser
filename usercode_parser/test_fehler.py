import unittest
from unittest import TestCase
from usercode_parser.fehler import Fehler, FehlerManager


class TestFehlerManager(TestCase):
    def test_print_help(self):
        f1 = Fehler("test1", 2, "test2")
        result = "[test1] in Zeile 2 folgender Fehler: test2"

        self.assertEqual(FehlerManager.printHelp(f1), result)

if __name__ == '__main__':
    unittest.main()