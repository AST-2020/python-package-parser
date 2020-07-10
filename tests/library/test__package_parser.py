import unittest
from unittest import TestCase
from src.library.parser import _package_parser


class Test_package_parser(TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_package_parser, self).__init__(*args, **kwargs)

    def test__is_package_installed(self):
        package_installed = _package_parser._is_package_installed("tests.library.TestDirectory.TestPackage")
        package_not_installed = _package_parser._is_package_installed("imaginary_not_installed_package")
        self.assertEqual(True, package_installed)
        self.assertEqual(False, package_not_installed)

    def test__walk_package(self):
        index = 0
        expected = [
            ["tests.library.TestDirectory.TestPackage_3.file1",
             "tests/library/TestDirectory/TestPackage_3/file1.py",
             "tests/library/TestDirectory/TestPackage_3/file1.pyi"],
            ["tests.library.TestDirectory.TestPackage_3.file2",
             "tests/library/TestDirectory/TestPackage_3/file2.py",
             "None"],
            ["tests.library.TestDirectory.TestPackage_3",
             "tests/library/TestDirectory/TestPackage_3/__init__.py",
             "None"]]

        actual = _package_parser._walk_package("tests.library.TestDirectory.TestPackage_3")
        for module_path, python_file, python_interface_file in actual:
            self.assertEqual(expected[index][0], module_path)
            tested_python_file ="tests/" + python_file.rsplit("/tests/")[1]
            self.assertEqual(expected[index][1], tested_python_file)
            if python_interface_file is not None:
                tested_python_interface_file = "tests/" + python_interface_file.rsplit("/tests/")[1]
            else:
                tested_python_interface_file = "None"
            self.assertIn(tested_python_interface_file, expected[index])
            expected[index].remove(tested_python_interface_file)
            index += 1

    def test_parse_package_not_included(self):
        package_parsed = _package_parser.parse_package("deadpool2")
        self.assertEqual(None, package_parsed)


    def test_parse_package_included(self):
        expected = ["tests.library.TestDirectory.TestPackage_3.file1",
                    "tests.library.TestDirectory.TestPackage_3.file2",
                    "tests.library.TestDirectory.TestPackage_3"]
        package_parsed = _package_parser.parse_package("tests.library.TestDirectory.TestPackage_3")
        all_modules = package_parsed.get_all_modules()
        self.assertEqual("tests.library.TestDirectory.TestPackage_3", package_parsed.get_name())
        for i in range(len(package_parsed.get_all_modules())):
            self.assertEqual(expected[i], all_modules[i].get_name())


    def test_parse_packages_not_included(self):
        packages_parsed = _package_parser.parse_packages(["deadpool2"])
        self.assertEqual(None, packages_parsed)

    def test_parse_packages_included_and_not_included(self):
        expected = ["tests.library.TestDirectory.TestPackage_3.file1",
                    "tests.library.TestDirectory.TestPackage_3.file2",
                    "tests.library.TestDirectory.TestPackage_3"]
        package_parsed = _package_parser.parse_packages(["tests.library.TestDirectory.TestPackage_3",
                                                        "la_casa_de_papel"])

        all_modules = package_parsed.get_all_modules()
        self.assertEqual("tests.library.TestDirectory.TestPackage_3", package_parsed.get_name())
        for i in range(len(package_parsed.get_all_modules())):
            self.assertEqual(expected[i], all_modules[i].get_name())

    def test_many_parse_packages_included(self):
        expected = ["tests.library.TestDirectory.TestPackage_3.file1",
                    "tests.library.TestDirectory.TestPackage_3.file2",
                    "tests.library.TestDirectory.TestPackage_3",
                    "tests.library.TestDirectory.TestPackage_4.file1",
                    "tests.library.TestDirectory.TestPackage_4"
                    ]

        package_parsed = _package_parser.parse_packages(["tests.library.TestDirectory.TestPackage_3",
                                                         "tests.library.TestDirectory.TestPackage_4"])

        self.assertEqual("tests.library.TestDirectory.TestPackage_3, tests.library.TestDirectory.TestPackage_4",
                         package_parsed.get_name())
        all_modules = package_parsed.get_all_modules()
        for i in range(len(package_parsed.get_all_modules())):
            self.assertEqual(expected[i], all_modules[i].get_name())


if __name__ == '__main__':
    unittest.main()
