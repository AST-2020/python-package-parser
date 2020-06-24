from collections import OrderedDict
from typing import List
from unittest import TestCase
from src.library.model._parameter import Parameter
from src.library.model._function import Function
from src.library.model._klass import Class


# def __init__(self, name: str, methods: List[Function] = None):


class TestClass(TestCase):
    def __init__(self, *args, **kwargs):
        self.klasses = []
        super(TestClass, self).__init__(*args, **kwargs)
        self.function1 = Function("function1", [Parameter("arg1"),
                                                Parameter("arg2", eval("int")),
                                                Parameter("arg3", None),
                                                Parameter("arg4", has_default=True, default=2.4)])
        self.function2 = Function("function1", [Parameter("arg2")])

        self.function3 = Function("empty_func", None)

        # class instances to test
        self.klasses.append(Class("klass0"))
        self.klasses.append(Class("klass1"))
        self.klasses[1].add_method(self.function1)
        self.klasses.append(Class("klass2"))
        self.klasses[2].add_method(self.function1)
        self.klasses[2].add_method(self.function2)
        self.klasses.append(Class("klass3", [self.function1]))
        self.klasses.append(Class("klass4", [self.function1, self.function2]))
        self.klasses.append(Class("klass5"))
        self.klasses[5].add_method(self.function3)
        self.klasses.append(Class("klass6"))
        self.klasses[6].add_method(self.function1)
        self.klasses[6].add_method(self.function3)

        # expected
        self.expected_result_for_methods_with_same_name = {"klass1": {}, "klass2": {}, "klass3": {}, "klass4": {},
                                                           "klass5": {}, "klass6": {}}
        self.expected_result_for_methods_with_same_name["klass1"]["function1"] = \
            ["def function1(arg1, arg2, arg3, arg4)"]

        self.expected_result_for_methods_with_same_name["klass2"]["function1"] = \
            ["def function1(arg1, arg2, arg3, arg4)", "def function1(arg2)"]

        self.expected_result_for_methods_with_same_name["klass3"]["function1"] = [
            "def function1(arg1, arg2, arg3, arg4)"]

        self.expected_result_for_methods_with_same_name["klass4"]["function1"] = \
            ["def function1(arg1, arg2, arg3, arg4)", "def function1(arg2)"]

        self.expected_result_for_methods_with_same_name["klass5"]["empty_func"] = ["def empty_func(None)"]
        self.expected_result_for_methods_with_same_name["klass6"]["empty_func"] = ["def empty_func(None)"]
        self.expected_result_for_methods_with_same_name["klass6"]["function1"] = [
            "def function1(arg1, arg2, arg3, arg4)"]

    def test_get_name(self):
        for i in range(len(self.klasses)):
            self.assertEqual(self.klasses[i].get_name(), "klass" + str(i))

    # get_methods_with_name was also tested inside the add_method
    def test_add_method(self):
        self.klas = Class("klass7")
        self.klas.add_method(self.function1)
        self.expected_result_for_methods_with_same_name = ["def function1(arg1, arg2, arg3, arg4)",
                                                           "def function1(arg2)"]

        for method in self.klas.get_methods_with_name("function1"):
            self.assertEqual(method.__str__(), "def function1(arg1, arg2, arg3, arg4)")

        self.klas.add_method(self.function2)
        method_list = self.klas.get_methods_with_name("function1")
        expected = ["def function1(arg1, arg2, arg3, arg4)", "def function1(arg2)"]
        for i in range(len(method_list)):
            self.assertEqual(method_list[i].__str__(), expected[i])

        self.klas.add_method(self.function3)
        for method in self.klas.get_methods_with_name("empty_func"):
            self.assertEqual(method.__str__(), "def empty_func(None)")

    def test_get_all_methods(self):
        for i in range(len(self.klasses)):
            if len(self.klasses[i].get_all_methods()) == 0:
                self.assertEqual(i, 0)
            else:
                method_lists = self.klasses[i].get_all_methods()

                for methods_with_same_name in method_lists:
                    for j in range(len(methods_with_same_name)):
                        method_name = methods_with_same_name[0].get_name()

                        self.assertEqual(methods_with_same_name[j].__str__() in self.
                                         expected_result_for_methods_with_same_name["klass" + str(i)][method_name],
                                         True)

                        self.assertEqual(len(methods_with_same_name),
                                         len(self.expected_result_for_methods_with_same_name["klass" + str(i)][
                                                 method_name]))
