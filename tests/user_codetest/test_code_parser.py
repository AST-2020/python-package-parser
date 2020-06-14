import unittest
import json
import ast

from user_code.model._variables import Variables
from user_code.model._imports import Imports
from user_code.parser import FunctionVisitor
from user_code.parser._function_parser import FunctionVisitor


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

        self.assertEqual(fv._get_name(node1), ('prefix', 'name'))
        self.assertEqual(fv._get_name(node2), ('', 'name'))
        self.assertEqual(fv._get_name(node3), ('pre1.pre2', 'name'))

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
        imp.add_import(name='t', package='torch', line=0)
        fv2 = FunctionVisitor(source, imp)
        self.assertEqual(('torch.onnx.symbolic_opset9', '', 'function'), fv2.expand_prefix('t', 1, 'randn'))

        # if is method
        imp = Imports()
        imp.add_import(name='torch', package='torch', line=0)
        vars = Variables()
        vars.add_usage('tensor', 1, 'torch.Tensor')
        fv3 = FunctionVisitor(source, imp, vars)
        self.assertEqual(('torch.tensor', 'Tensor', 'method'), fv3.expand_prefix('tensor', 1, 'norm'))

        # if is Constructor with alias
        imp = Imports()
        imp.add_import(name='torch', package='torch', line=0)
        fv4 = FunctionVisitor(source, imp)
        self.assertEqual(('torch.tensor', 'Tensor', 'method'), fv4.expand_prefix('torch', 1, 'Tensor'))

        # if Constructor without alias
        imp = Imports()
        imp.add_unnamed_import(package='torch', line=0)
        fv4 = FunctionVisitor(source, imp)
        self.assertEqual(('torch.tensor', 'Tensor', 'method'), fv4.expand_prefix('', 2, 'Tensor'))

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
