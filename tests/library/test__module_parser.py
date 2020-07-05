from unittest import TestCase
from src.library.parser._package_parser import parse_package


class Test_PythonFileVisitor(TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_PythonFileVisitor, self).__init__(*args, **kwargs)
        self.result_package = parse_package("tests.library.TestDirectory.TestPackage_2")

    # UC1
    def test_UC1_method_with_parameter(self):
        methods_with_same_name = self.result_package.get_methods_with_name("tests.library.TestDirectory.TestPackage_2.UC1",
                                                                           "test_class1", "method_uc1")
        for method in methods_with_same_name:
            self.assertEqual("def method_uc1(arg_method_3, arg_method_4)", method.__str__())

    def test_UC1_method_without_parameter(self):
        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC1",
            "test_class1", "method2_uc1")
        for method in methods_with_same_name:
            self.assertEqual("def method2_uc1()", method.__str__())

    def test_UC1_function_with_parameter(self):
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC1", "test_func_1")
        for function in functions_with_same_name:
            self.assertEqual("def test_func_1(arg_func_1, arg_func_2)", function.__str__())

    def test_UC1_function_without_parameter(self):
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC1", "test_func_2")
        for function in functions_with_same_name:
            self.assertEqual("def test_func_2()", function.__str__())

    # UC2_and_3
    def test_UC2_and_3_method_with_parameter(self):
        expected = ["arg_method_1", "arg_method_2 = 2", "arg_method_3 = 10.4", "arg_method_4 = True",
                    "arg_method_5 = []", "arg_method_6 = []", "arg_method_7 = []", "arg_method_8 = None]"]

        methods_with_same_name = self.result_package.get_methods_with_name("tests.library.TestDirectory.TestPackage_2.UC2_and_3",
                                                                           "test_class1", "method_uc1")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i+1], method.get_parameters()[i].__str__())

    def test_UC2_and_3_method_without_parameter(self):
        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC2_and_3",
            "test_class1", "method2_uc2")
        for method in methods_with_same_name:
            self.assertEqual("def method2_uc2()", method.__str__())

    def test_UC2_and_3_function_with_parameter(self):
        expected =["arg_func_0", "arg_func_1 = 2", "arg_func_2 = 10.4", "arg_func_3 = True", "arg_func_4 = []",
                   "arg_func_5 = []", "arg_func_6 = []", "arg_func_7 = None"]
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC2_and_3", "test_func_1")

        for function in functions_with_same_name:
            for i in range(len(function.get_parameters())):
                self.assertEqual(expected[i], function.get_parameters()[i].__str__())

    def test_UC2_and_3_function_without_parameter(self):
        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC2_and_3", "test_func_2")
        for function in functions_with_same_name:
            self.assertEqual("def test_func_2()", function.__str__())

    # UC4 (type hints in py)
    def test_UC4_primitive_py_type_hints_in_methods(self):
        expected = ["my_int: <class 'int'>", "my_dict: typing.Dict", "my_bool: <class 'bool'> = True",
                    "my_float: <class 'float'> = 2.5"]
        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pi_files", "testFile4", "__init__")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    def test_UC4_py_type_hints_from_typing_in_methods(self):
        expected = ["my_union: typing.Union[int, bool]", "my_optional: typing.Union[int, NoneType]",
                    "my_callable: typing.Callable[[torch.Tensor], NoneType]"]
        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pi_files", "testFile4", "method_for_testFile4")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    def test_UC4_primitive_py_type_hints_in_functions(self):
        expected = ["param_0: typing.Any",
                    "param_1: typing.Union[int, NoneType]",
                    "param_2: typing.Callable[[torch.Tensor, torch.Tensor, int], torch.Tensor]",
                    "param_3: typing.Callable[..., torch.Tensor]"]
        methods_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pi_files", "testFunc4")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    def test_UC4_py_type_hints_from_typing_in_functions(self):
        expected = ["param_0: typing.Dict[float, typing.Any]",
                    "param_1: typing.Callable[[torch.Tensor, torch.Tensor, int], torch.Tensor]", "param_2"]
        methods_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pi_files", "testFunc41")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    # UC4 (type_hints_from_pyi_files)
    def test_UC4_pyi_type_hints_ex1_in_methods(self):
        expected = ["name: typing.Union[typing.Any, str, int, NoneType]", "nachname: typing.Union[int, NoneType]",
                    "echte_name: typing.Callable[[torch.Tensor, torch.Tensor, int], torch.Tensor]"]

        methods_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "__init__")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    def test_UC4_pyi_type_hints_ex2_in_methods(self):
        expected = ["num: <class 'int'>", "my_list: typing.List", "my_bool: <class 'bool'>",
                    "my_double: <class 'float'>", "stringy: <class 'str'>", "my_obj: typing.Any"]

        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "testFile5", "method_50")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    def test_UC4_pyi_type_hints_ex3_in_methods(self):
        expected = ["name: typing.Dict[float, typing.Any]",
                    "nachname: typing.Callable[[torch.Tensor, torch.Tensor, int], torch.Tensor]", "echte_name"]

        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "testFile5", "method_51")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    def test_UC4_pyi_type_hints_ex4_in_methods(self):
        expected = [["name: typing.Union[int, torch.Tensor]", "nachname: typing.Callable[..., torch.Tensor]",
                     "echte_name: typing.Callable[[typing.Any], NoneType]"],
                    ["name: <class 'int'>", "nachname: <class 'torch.Tensor'>", "echte_name: <class 'NoneType'>"],
                    ["name2: <class 'int'>", "nachname2", "echte_name2"]
                    ]

        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "testFile5", "method_52")
        for i in range(len(methods_with_same_name)):
            for j in range(len(methods_with_same_name[i].get_parameters())):
                self.assertEqual(expected[i][j], methods_with_same_name[i].get_parameters()[j].__str__())

    def test_hint_already_found_in_py(self):
        expected = ["name", "nachname: <class 'str'> = yoyoyo", "echte_name = kein Witz"]

        methods_with_same_name = self.result_package.get_methods_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "testFile5", "method_53")
        for method in methods_with_same_name:
            for i in range(len(method.get_parameters())):
                self.assertEqual(expected[i], method.get_parameters()[i].__str__())

    def test_UC4_pyi_type_hints_ex1_in_functions(self):
        expected = [["num: <class 'str'>", "my_list: typing.List", "my_bool: <class 'bool'>",
                     "my_double: <class 'float'>", "my_obj: typing.Any"],
                    ["num: <class 'str'>", "my_list: typing.Dict", "my_bool: <class 'bool'>" ,"my_double: typing.Any",
                     "my_obj: typing.Any"]
                    ]

        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "testFunc51")
        for i in range(len(functions_with_same_name)):
            for j in range(len(functions_with_same_name[i].get_parameters())):
                self.assertEqual(expected[i][j], functions_with_same_name[i].get_parameters()[j].__str__())

    def test_UC4_pyi_type_hints_ex2_in_functions(self):


        functions_with_same_name = self.result_package.get_top_level_functions_with_name(
            "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "testFunc52")
        for i in range(len(functions_with_same_name)):
            for j in range(len(functions_with_same_name[i].get_parameters())):
                self.assertEqual(expected[i][j], functions_with_same_name[i].get_parameters()[j].__str__())