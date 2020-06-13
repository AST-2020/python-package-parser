import unittest
from unittest import TestCase

from messages.fehler import Fehler, FehlerManager


class TestFehlerManager(TestCase):
    def test_print_help(self):
        f1 = Fehler("Pfad", 2, "Beschreibung", "Datei")
        result = "error occured  in [Pfad in file Datei] in line 2: Beschreibung"

        self.assertEqual(str(f1), result)

if __name__ == '__main__':
    unittest.main()