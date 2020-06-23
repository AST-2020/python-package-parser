from typing import List
from unittest import TestCase
from library.model._parameter import Parameter
from library.model._function import Function
from library.model._klass import Class


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
        self.klasses.append(Class("klass1", [self.function1, self.function2]))
        self.klasses.append(Class("klass2", [self.function1, self.function1, self.function2]))
        self.klasses.append(Class("klass3", [self.function2]))
        self.klasses.append(Class("klass4", [self.function2]))
        self.klasses.append(Class("klass5", []))

        # expected

    def test_get_name(self):
        for i in range(len(self.klasses)):
            self.assertEqual(self.klasses[i].get_name(), "klass"+str(i+1))

    # def test_add_method(self):
    #     self.fail()

    # def test_get_methods_with_name(self):
    #     self.fail()
    #
    # def test_get_all_methods(self):
    #     self.fail()


