import unittest
from unittest import TestCase
from src.library.model._parameter import Parameter
from torch import Tensor


class TestParameter(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestParameter, self).__init__(*args, **kwargs)
        self.parameters = []
        self.parameters.append(Parameter("arg1"))
        self.parameters.append(Parameter("arg2", eval("Tensor")))
        self.parameters.append(Parameter("arg3", eval("int")))
        self.parameters.append(Parameter("arg4", None))
        self.parameters.append(Parameter("arg5", has_default=True, default=None))
        self.parameters.append(Parameter("arg6", has_default=True, default=True))
        self.parameters.append(Parameter("arg7", has_default=False, default=None))
        self.parameters.append(Parameter("arg8", eval("float"), True, 2))

        # expected results
        self.type_hints = [None, eval("Tensor"), eval("int"), None, None, None, None, eval("float")]
        self.has_defaults = [False, False, False, False, True, True, False, True]
        self.defaults = [None, None, None, None, None, True, None, 2]

    def test_get_name(self):
        for i in range(len(self.parameters)):
            self.assertEqual(self.parameters[i].get_name(), ("arg" + str(i + 1)))

    def test_get_type_hint(self):
        for i in range(len(self.parameters)):
            self.assertEqual(self.parameters[i].get_type_hint(), self.type_hints[i])

    def test_has_default(self):
        for i in range(len(self.parameters)):
            self.assertEqual(self.parameters[i].has_default(), self.has_defaults[i])

    def test_get_default(self):
        for i in range(len(self.parameters)):
            self.assertEqual(self.parameters[i].get_default(), self.defaults[i])


if __name__ == '__main__':
    unittest.main()
