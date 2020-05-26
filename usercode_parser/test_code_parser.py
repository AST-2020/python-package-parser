import unittest
import json
import ast

from variables import UsedVariables
from imports import Imports
from variable_parser import VariableVisitor
from code_parser import FunctionVisitor


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

        self.assertEqual(fv.get_name(node1), ('prefix', 'name'))
        self.assertEqual(fv.get_name(node2), ('', 'name'))
        self.assertEqual(fv.get_name(node3), ('pre1.pre2', 'name'))

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
        # get souce structure depending on torch or sklearn selected
        with open('resultsPytorch.txt') as json_file:
            json_obj = json.load(json_file)
        source = json.loads(json_obj)

        fv = FunctionVisitor(source)



    def test_get_keywords(self):
        text1 = "func(a=1, b=2)"
        tree1 = ast.parse(text1)
        node1 = tree1.body[0].value

        text2 = "func(1, 2)"
        tree2 = ast.parse(text2)
        node2 = tree2.body[0].value

        fv = FunctionVisitor({})

        self.assertListEqual(fv.get_keywords(node1), ['a', 'b'])
        self.assertListEqual(fv.get_keywords(node2), [])
