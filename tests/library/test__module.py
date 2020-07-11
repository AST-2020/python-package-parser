from unittest import TestCase
from src.library.model._module import Module
from src.library.model._klass import Class
from src.library.model._function import Function
from src.library.model._parameter import Parameter


class TestModule(TestCase):
    def test_multiple_classes_with_same_name(self):
        expected = ["def func1()", "def func2()"]

        klass1 = Class("klass_1", [Function("func1", [])])
        klass2 = Class("klass_1", [Function("func2", [])])

        module = Module("module_1")
        module.add_class(klass1)
        module.add_class(klass2)

        for klass in module.get_classes_with_name("klass_1"):
            func_name = klass.get_all_methods()[0][0].__str__()
            self.assertIn(func_name, expected)
            expected.remove(func_name)

    def test_multiple_funcs_with_same_name(self):
        expected = ["param_1", "param_2"]

        func1 = Function("func_1", [Parameter("param_1")])
        func2 = Function("func_1", [Parameter("param_2")])

        module = Module("module_1")
        module.add_top_level_function(func1)
        module.add_top_level_function(func2)

        for func in module.get_top_level_functions_with_name("func_1"):
            param_name = func.get_parameters()[0].__str__()
            self.assertIn(param_name, expected)
            expected.remove(param_name)
