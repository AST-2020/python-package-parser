from typing import List
from unittest import TestCase
from src.library.model._parameter import Parameter
from src.library.model._function import Function


def set_results(parameters: List[Parameter]) -> List[str]:
    returned_results = []
    for parameter in parameters:
        returned_results.append(parameter.__str__())
    return returned_results


class TestFunction(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFunction, self).__init__(*args, **kwargs)
        self.parameters = []
        self.parameters.append(Parameter("arg1"))
        self.parameters.append(Parameter("arg2", eval("int")))
        self.parameters.append(Parameter("arg3", None))
        self.parameters.append(Parameter("arg4", has_default=True, default=2.4))
        self.parameters.append(Parameter("arg5", has_default=False, default=None))
        self.parameters.append(Parameter("arg6", eval("float"), True, 2))

        # test functions
        self.function1 = Function("function1", self.parameters)
        self.function2 = Function("empty_func", None)

        self.expected_results = set_results(self.parameters)

    def test_get_name(self):
        self.assertEqual(self.function1.get_name(), "function1")
        self.assertEqual(self.function2.get_name(), "empty_func")

    def test_get_parameter(self):
        for i in range(len(self.parameters)):
            self.assertEqual(self.function1.get_parameter("arg" + str(i + 1)).__str__(), self.expected_results[i])

    def test_get_parameters(self):
        actual_parameters = self.function1.get_parameters()
        for i in range(len(actual_parameters)):
            self.assertEqual(actual_parameters[i].__str__(), self.expected_results[i])
        self.assertEqual(self.function2.get_parameters(), None)
