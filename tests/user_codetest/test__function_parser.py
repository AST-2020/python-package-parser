from user_code.model.variable import Variable
from user_code.model.argument import Arg

import unittest
import ast

from user_code.parser._function_parser import FunctionVisitor


class UserCodeCase(unittest.TestCase):
    def test__get_positional_arg(self):

        var = Variable('N', 13, 64)
        var2 = Variable('D_in', 13, 1000)
        var3 = Variable('H', 13, 100)
        var4 = Variable('D_out', 13, 10)
        var5 = Variable('N', 20, 3)

        declared_vars = []
        declared_vars.append(var)
        declared_vars.append(var2)
        declared_vars.append(var3)
        declared_vars.append(var4)
        declared_vars.append(var5)

        exp_args = []

        text = 'f(1,2,True)'
        tree = ast.parse(text)
        exp_args.append(Arg(1))
        exp_args.append(Arg(2))
        exp_args.append(Arg(True))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                args = FunctionVisitor._get_positional_arg(node, declared_vars)

        self.asser(args, exp_args)
        exp_args_value = [arg.value for arg in exp_args]
        exp_args_type =  [arg.type for arg in exp_args]
        for arg in args:
            # self.assertIn(arg, exp_args)
            self.assertSetEqual()
            self.assertL
            self.assertIn(arg.type, exp_args_type)
            self.assertIn(arg.value, exp_args_value)

        text = 'f(False, 5.7, "str")'
        tree = ast.parse(text)
        exp_args.append(Arg(False))
        exp_args.append(Arg(5.7))
        exp_args.append(Arg('str'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                args = FunctionVisitor._get_positional_arg(node, declared_vars)

        # self.asser(args, exp_args)
        exp_args_value = [arg.value for arg in exp_args]
        exp_args_type = [arg.type for arg in exp_args]
        for arg in args:
            # self.assertIn(arg, exp_args)
            self.assertIn(arg.type, exp_args_type)
            self.assertIn(arg.value, exp_args_value)

    def test__get_keyword_arg(self):
        assert True
