import unittest
from unittest import TestCase
from StrukturImplementation.ast_test.struktur_implementation import Structure

class TestStructure(TestCase):
    def test_to_json(self):
        result = '{\n\t\t "function": {},\n\t\t "method": {},\n\t\t "package__all__list": {}\n }'
        teststructure = Structure()

        self.assertEqual(result, teststructure.toJSON(teststructure.dict))

if __name__ == '__main__':
    unittest.main()