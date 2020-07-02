from user_code.model.variable import Variable
from user_code.model.argument import Arg, Kw_arg

import unittest
import ast

from user_code.parser._function_parser import FunctionVisitor


class UserCodeCase(unittest.TestCase):

    @staticmethod
    def convert_arg_to_List(args):
        tuple = [(arg.value, arg.type) for arg in args]
        return tuple

    @staticmethod
    def convert_kw_arg_to_List(kw_args):
        tuple = [(arg.name,arg.value, arg.type) for arg in kw_args]
        return tuple

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

        # this is the first set of tested elements
        exp_args = []
        exp_args.append((1,type(1)))
        exp_args.append((2,type(2)))
        exp_args.append((True, type(True)))

        text = 'f(1,2,True)'
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                args = FunctionVisitor._get_positional_arg(node, declared_vars)
        arg_list = UserCodeCase.convert_arg_to_List(args)
        self.assertListEqual(arg_list, exp_args)

        # this ist the second set of tested elements
        exp_args = []
        exp_args.append((False, type(False)))
        exp_args.append((5.7, type(5.7)))
        exp_args.append(('str', type('str')))

        text = 'f(False, 5.7, "str")'
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                args = FunctionVisitor._get_positional_arg(node, declared_vars)
        arg_list = UserCodeCase.convert_arg_to_List(args)
        self.assertListEqual(arg_list, exp_args)

        # for arg in args:
        #     print(arg.value)
        # self.assertSequenceEqual(args, exp_args)
        # self.assertSequenceEqual(args, exp_args, 'hello', None)

        # exp_args_value = [arg.value for arg in exp_args]
        # exp_args_type =  [arg.type for arg in exp_args]
        # for arg in args:
        #     # self.assertIn(arg, exp_args)
        #     self.assertIn(arg.type, exp_args_type)
        #     self.assertIn(arg.value, exp_args_value)
        #
        # text = 'f(False, 5.7, "str")'
        # tree = ast.parse(text)
        # exp_args.append(Arg(False))
        # exp_args.append(Arg(5.7))
        # exp_args.append(Arg('str'))
        # for node in ast.walk(tree):
        #     if isinstance(node, ast.Call):
        #         args = FunctionVisitor._get_positional_arg(node, declared_vars)
        #
        # # self.asser(args, exp_args)
        # # self.assertSetEqual(args, exp_args)
        #
        # # self.assertSequenceEqual(args, exp_args)
        #
        # exp_args_value = [arg.value for arg in exp_args]
        # exp_args_type = [arg.type for arg in exp_args]
        # for arg in args:
        #     # self.assertIn(arg, exp_args)
        #     self.assertIn(arg.type, exp_args_type)
        #     self.assertIn(arg.value, exp_args_value)

    def test__get_keyword_arg(self):

        # list of Objects of Variable to give to the mathod
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

        # this is the first set of tested elements
        exp_args = []
        exp_args.append(('a',1, type(1)))
        exp_args.append(('b',2, type(2)))
        exp_args.append(('c',True, type(True)))

        text = 'f(a=1, b=2, c=True)'
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                kw_args = FunctionVisitor._get_keyword_arg(node, declared_vars)
        kw_arg_list = UserCodeCase.convert_kw_arg_to_List(kw_args)
        self.assertListEqual(kw_arg_list, exp_args)

        # this ist the second set of tested elements
        exp_args = []
        exp_args.append(('a', False, type(False)))
        exp_args.append(('b', 5.7, type(5.7)))
        exp_args.append(('c', 'str', type('str')))

        text = 'f(a=False, b=5.7, c="str")'
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                kw_args = FunctionVisitor._get_keyword_arg(node, declared_vars)
        kw_arg_list = UserCodeCase.convert_kw_arg_to_List(kw_args)
        self.assertListEqual(kw_arg_list, exp_args)


if __name__ == '__main__':
    unittest.main()