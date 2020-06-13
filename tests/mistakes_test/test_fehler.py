import unittest
from unittest import TestCase

from analyses.messages.fehler import Message


class TestFehlerManager(TestCase):
    def test_print_help(self):
        f1 = Message("Pfad", 2, "Beschreibung", "Datei")
        result = "error occured  in [Pfad in file Datei] in line 2: Beschreibung"

        self.assertEqual(str(f1), result)

if __name__ == '__main__':
    unittest.main()