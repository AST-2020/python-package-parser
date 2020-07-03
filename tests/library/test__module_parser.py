from unittest import TestCase
from src.library.parser._package_parser import parse_package


class Test_PythonFileVisitor(TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_PythonFileVisitor, self).__init__(*args, **kwargs)
        self.result_package = parse_package("tests.library.TestDirectory.TestPackage_2")

    # UC1
    def test_UC1_constructor_with_parameter(self):
        methods_with_same_name = self.result_package.get_methods_with_name("tests.library.TestDirectory.TestPackage_2.UC1",
                                                               "test_class1", "__init__")
        for method in methods_with_same_name:
            self.assertEqual(method.__str__(), "def __init__(arg_method_1, arg_method_2)")

    def test_UC1_method_with_parameter(self):
        methods_with_same_name = self.result_package.get_methods_with_name("tests.library.TestDirectory.TestPackage_2.UC1",
                                                                           "test_class1", "method_uc1")
        for method in methods_with_same_name:
            self.assertEqual(method.__str__(), "def method_uc1(arg_method_3, arg_method_4)")

    def test_UC1_method_without_parameter(self):
        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC1",
            "test_class1", "method2_uc1")
        for method in methods_with_same_name:
            self.assertEqual(method.__str__(), "def method2_uc1()")

    def test_UC1_function_with_parameter(self):
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC1", "test_func_1")
        for function in functions_with_same_name:
            self.assertEqual(function.__str__(), "def test_func_1(arg_func_1, arg_func_2)")

    def test_UC1_function_without_parameter(self):
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC1", "test_func_2")
        for function in functions_with_same_name:
            self.assertEqual(function.__str__(), "def test_func_2()")

    # UC2_and_3
    def test_UC2_and_3_constructor_with_parameter(self):
        expected = ["arg_method_init_1", "arg_method_init_2 = foo"]
        methods_with_same_name = self.result_package.get_methods_with_name("tests.library.TestDirectory.TestPackage_2.UC2_and_3",
                                                               "test_class1", "__init__")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(method.get_parameters()[i], expected[i + 1])

    def test_UC2_and_3_method_with_parameter(self):
        expected = ["arg_method_1", "arg_method_2 = 2", "arg_method_3 = 10.4", "arg_method_4 = True",
                    "arg_method_5 = []", "arg_method_6 = []", "arg_method_7 = []", "arg_method_8 = None]"]

        methods_with_same_name = self.result_package.get_methods_with_name("tests.library.TestDirectory.TestPackage_2.UC2_and_3",
                                                                           "test_class1", "method_uc1")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(method.get_parameters()[i].__str__(), expected[i+1])

    def test_UC2_and_3_method_without_parameter(self):
        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC2_and_3",
            "test_class1", "method2_uc2")
        for method in methods_with_same_name:
            self.assertEqual(method.__str__(), "def method2_uc2()")

    def test_UC2_and_3_function_with_parameter(self):
        expected =["arg_func_0", "arg_func_1 = 2", "arg_func_2 = 10.4", "arg_func_3 = True", "arg_func_4 = []",
                   "arg_func_5 = []", "arg_func_6 = []", "arg_func_7 = None"]
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC2_and_3", "test_func_1")

        for function in functions_with_same_name:
            for i in range(len(function.get_parameters())):
                self.assertEqual(function.get_parameters()[i].__str__(), expected[i])

    def test_UC2_and_3_function_without_parameter(self):
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC2_and_3", "test_func_2")
        for function in functions_with_same_name:
            self.assertEqual(function.__str__(), "def test_func_2()")
