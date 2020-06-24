from unittest import TestCase
import ast
import TestPackage_2
from TestPackage_2 import UC1
from src.library.parser._package_parser import _walk_package


class Test_PythonFileVisitor(TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_PythonFileVisitor, self).__init__(*args, **kwargs)
        for module_path, python_file, python_interface_file in _walk_package("TesPackage_2/UC1"):
            print(module_path, " ", python_file, " ", python_interface_file)

    # in visit_function_def:
    # 1- test for property decorator
    # 2- adding functions and methods with and without parameters
    ####
    # in find_type_hint:
    # 1- test for different types of type_hints in py and pyi files
    ####



    # def test_visit_function_def(self):
    #     pass

    # def test_find_inner_hint(self):
    #     self.fail()
