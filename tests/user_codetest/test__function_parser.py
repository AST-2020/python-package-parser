
from src.user_code.parser import FunctionVisitor
from src.user_code.model.variable import Variable
from src.user_code.model.argument import Arg


import unittest
import json
import ast

from src.user_code.model._variables import Variables
from src.user_code.model._imports import Imports
from src.user_code.parser import FunctionVisitor
from src.user_code.parser._function_parser import FunctionVisitor


class UserCodeCase(unittest.TestCase):
    def test_get_name(self):
        text1 = "prefix.name()"
        tree1 = ast.parse(text1)
        node1 = tree1.body[0].value

        text2 = "name()"
        tree2 = ast.parse(text2)
        node2 = tree2.body[0].value

        text3 = "pre1.pre2.name()"
        tree3 = ast.parse(text3)
        node3 = tree3.body[0].value

        fv = FunctionVisitor({})

        self.assertEqual(fv._get_function_receiver(node1), ('prefix', 'name'))
        self.assertEqual(fv._get_function_receiver(node2), ('', 'name'))
        self.assertEqual(fv._get_function_receiver(node3), ('pre1.pre2', 'name'))

    def test_get_path(self):
        # get souce structure depending on torch or sklearn selected
        with open('resultsPytorch.txt') as json_file:
            json_obj = json.load(json_file)
        source = json.loads(json_obj)

        fv = FunctionVisitor(source)

        self.assertEqual(fv.get_path('torch', 'randn', 'function'), 'torch.onnx.symbolic_opset9')
        self.assertEqual(fv.get_path('torch.onnx.symbolic_opset9.randn', 'randn', 'function'),
                         'torch.onnx.symbolic_opset9')

        self.assertEqual(fv.get_path('torch', 'norm', 'method', 'Tensor'), 'torch.tensor')
        self.assertEqual(fv.get_path('torch.tensor.Tensor.norm', 'norm', 'method', 'Tensor'),
                         'torch.tensor')

        self.assertEqual(fv.get_path(None, '', ''), '')

    def test_expand_prefix(self):
        # get souce structure
        with open('resultsPytorch.txt') as json_file:
            json_obj = json.load(json_file)
        source = json.loads(json_obj)

        # if prefix is None
        fv1 = FunctionVisitor(source)
        self.assertEqual(('', '', ''), fv1.expand_prefix(None, 1, ''))

        # if is function
        imp = Imports()
        imp.add_import(alias='t', full_name='torch', line=0)
        fv2 = FunctionVisitor(source, imp)
        self.assertEqual(('torch.onnx.symbolic_opset9', '', 'function'), fv2.expand_prefix('t', 1, 'randn'))

        # if is method
        imp = Imports()
        imp.add_import(alias='torch', full_name='torch', line=0)
        vars = Variables()
        vars.add_usage('tensor', 1, 'torch.Tensor')
        fv3 = FunctionVisitor(source, imp, vars)
        self.assertEqual(('torch.tensor', 'Tensor', 'method'), fv3.expand_prefix('tensor', 1, 'norm'))

        # if is Constructor with alias
        imp = Imports()
        imp.add_import(alias='torch', full_name='torch', line=0)
        fv4 = FunctionVisitor(source, imp)
        self.assertEqual(('torch.tensor', 'Tensor', 'method'), fv4.expand_prefix('torch', 1, 'Tensor'))

    def test_get_keywords(self):
        text1 = "func(a=1, b=2)"
        tree1 = ast.parse(text1)
        node1 = tree1.body[0].value

        text2 = "func(1, 2)"
        tree2 = ast.parse(text2)
        node2 = tree2.body[0].value

        fv = FunctionVisitor({})

        self.assertListEqual(FunctionVisitor._get_keyword_arg_names(fv), ['a', 'b'])
        self.assertListEqual(FunctionVisitor._get_keyword_arg_names(fv), [])


    def test__get_positional_arg(self):
        text = 'f(1,2,3)'
        arg= []
        arg.append(Arg(1,type(1)))
        arg.append(Arg(2,type(2)))
        arg.append(Arg(3, type(3)))

        tree = ast.parse(text)

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

        expe

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                args = FunctionVisitor._get_positional_arg(node, declared_vars)

        self.assertListEqual(args, args)
