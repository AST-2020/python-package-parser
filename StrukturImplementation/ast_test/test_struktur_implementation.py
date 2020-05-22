import unittest
from unittest import TestCase
from StrukturImplementation.ast_test.struktur_implementation import Structure

class TestStructure(TestCase):

    def test_add_module_path(self):
        st1 = Structure()

        #Schluesselwort None ist ungueltig
        try:
            st1.add_module_path("method", None)
        except KeyError:
            self.fail("add_module_path(None) ist nicht gueltig")

        try:
            st1.add_module_path("function", None)
        except KeyError:
            self.fail("add_module_path(\"function\", None) ist nicht gueltig")

        #Leerer String ist ungueltig
        try:
            st1.add_module_path("method", "")
        except KeyError:
            self.fail("add_module_path(\"\") ist nciht gueltig")

        try:
            st1.add_module_path("function", "")
        except KeyError:
            self.fail("add_module_path(\"function\", \"\")")

    def test_add_class_name(self):
        st1 = Structure()
        # Schluesselwort None ist ungueltig
        try:
            st1.add_module_path("method", None)
        except KeyError:
            self.fail("add_module_path(None) ist nicht gueltig")

        try:
            st1.add_module_path("function", None)
        except KeyError:
            self.fail("add_module_path(\"function\", None) ist nicht gueltig")

        # Leerer String ist ungueltig
        try:
            st1.add_module_path("method", "")
        except KeyError:
            self.fail("add_module_path(\"\") ist nciht gueltig")

        try:
            st1.add_module_path("function", "")
        except KeyError:
            self.fail("add_module_path(\"function\", \"\")")

    def test_add_method(self):
        st1 = Structure()
        # Schluesselwort None ist ungueltig
        try:
            st1.add_module_path("method", None)
        except KeyError:
            self.fail("add_module_path(None) ist nicht gueltig")

        try:
            st1.add_module_path("function", None)
        except KeyError:
            self.fail("add_module_path(\"function\", None) ist nicht gueltig")

        # Leerer String ist ungueltig
        try:
            st1.add_module_path("method", "")
        except KeyError:
            self.fail("add_module_path(\"\") ist nciht gueltig")

        try:
            st1.add_module_path("function", "")
        except KeyError:
            self.fail("add_module_path(\"function\", \"\")")

    def test_add_func(self):
        st1 = Structure()
        # Schluesselwort None ist ungueltig
        try:
            st1.add_module_path("method", None)
        except KeyError:
            self.fail("add_module_path(None) ist nicht gueltig")

        try:
            st1.add_module_path("function", None)
        except KeyError:
            self.fail("add_module_path(\"function\", None) ist nicht gueltig")

        # Leerer String ist ungueltig
        try:
            st1.add_module_path("method", "")
        except KeyError:
            self.fail("add_module_path(\"\") ist nciht gueltig")

        try:
            st1.add_module_path("function", "")
        except KeyError:
            self.fail("add_module_path(\"function\", \"\")")

    def test_add__all__(self):
        st1 = Structure()
        # Schluesselwort None ist ungueltig
        try:
            st1.add_module_path("method", None)
        except KeyError:
            self.fail("add_module_path(None) ist nicht gueltig")

        try:
            st1.add_module_path("function", None)
        except KeyError:
            self.fail("add_module_path(\"function\", None) ist nicht gueltig")

        # Leerer String ist ungueltig
        try:
            st1.add_module_path("method", "")
        except KeyError:
            self.fail("add_module_path(\"\") ist nciht gueltig")

        try:
            st1.add_module_path("function", "")
        except KeyError:
            self.fail("add_module_path(\"function\", \"\")")

    def test_to_json(self):
        result = '{\n "function": {},\n "method": {},\n "package__all__list": {}\n}'
        teststructure = Structure()
        test = teststructure.toJSON(teststructure.dict)

        self.assertEqual(' '.join(result.split()), ' '.join(test.split()))

if __name__ == '__main__':
    unittest.main()