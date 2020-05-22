import unittest
from unittest import TestCase
from StrukturImplementation.ast_test.struktur_implementation import Structure

class TestStructure(TestCase):
    def test_to_json(self):
        result = '{\n "function": {},\n "method": {},\n "package__all__list": {}\n}'
        teststructure = Structure()
        test = teststructure.toJSON(teststructure.dict)

        self.assertEqual(' '.join(result.split()), ' '.join(test.split()))

if __name__ == '__main__':
    unittest.main()