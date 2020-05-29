import unittest
from unittest import TestCase

from mistakes.fehler import Fehler, FehlerManager


class TestFehlerManager(TestCase):
    def test_print_help(self):
        f1 = Fehler("Pfad", 2, "Beschreibung", "Datei")
        result = "[Pfad in Datei Datei] in Zeile 2 folgender Fehler: Beschreibung"

        self.assertEqual(FehlerManager.printHelp(f1), result)

if __name__ == '__main__':
    unittest.main()