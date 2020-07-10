import unittest
from unittest import TestCase
from .TestDirectory import TestPackage
from src.library.parser import _package_parser


class Test(TestCase):

    def test__walk_package(self):
        parsed_package = _package_parser._walk_package("TestPackage")
        for module_path, python_file, python_interface_file in parsed_package:
            if "TestPackage.UC4_pyi_files.py" in python_file:
                self.assertEqual("TestPackage.UC4_pyi_files.pyi" in python_interface_file, True)
            elif "TestPackage.UC4_py_files.py" in python_file:
                self.assertEqual(python_interface_file, None)

    def test_parse_package(self):
        pass

    # def test_parse_packages(self):
    #     self.fail()

    def test__is_package_installed(self):
        package_installed = _package_parser._is_package_installed("TestPackage")
        package_not_installed = _package_parser._is_package_installed("imaginary_not_installed_package")
        self.assertEqual(package_installed, True)
        self.assertEqual(package_not_installed, False)


if __name__ == '__main__':
    unittest.main()
