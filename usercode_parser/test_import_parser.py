import unittest
from import_parser import ImportVisitor
from imports import Imports
import json
import ast


class ImportParserTestCase(unittest.TestCase):
    def test_get_package_from_content(self):
        imp = Imports()
        imp.add_unnamed_import('x', 1)
        imp.set_package_content('x', ['a'])

        # check if package is found for content
        self.assertEqual('x', imp.get_package_from_content('a',2))
        # check if not inclouded name returns None
        self.assertIs(imp.get_package_from_content('b',2), None)

    def test_visit_Import(self):
        test_code1 = 'import torch'
        test_code2 = 'import torch as t'
        test_code3 = 'import torch as t, numpy as np'
        test_code4 = 'import torch.nn as nn'
        test_code5 = 'import torch.nn'

        # get souce structure depending on torch or sklearn selected
        with open('resultsPytorch.txt') as json_file:
            json_obj = json.load(json_file)
        source = json.loads(json_obj)

        imp = ImportVisitor('torch', source)

        tree = ast.parse(test_code1)
        imp.visit(tree)
        self.assertIn('torch', imp.get_imports().named)
        self.assertIn('torch', imp.get_imports().named['torch'])
        imp.del_imports()

        tree = ast.parse(test_code2)
        imp.visit(tree)
        self.assertIn('t', imp.get_imports().named)
        self.assertIn('torch', imp.get_imports().named['t'])
        imp.del_imports()

        tree = ast.parse(test_code3)
        imp.visit(tree)
        self.assertIn('t', imp.get_imports().named)
        self.assertIn('torch', imp.get_imports().named['t'])
        self.assertNotIn('np', imp.get_imports().named)
        self.assertNotIn('numpy', imp.get_imports().named)
        imp.del_imports()

        tree = ast.parse(test_code4)
        imp.visit(tree)
        self.assertIn('nn', imp.get_imports().named)
        self.assertIn('torch.nn', imp.get_imports().named['nn'])
        imp.del_imports()

        tree = ast.parse(test_code5)
        imp.visit(tree)
        self.assertIn('nn', imp.get_imports().named)
        self.assertIn('torch.nn', imp.get_imports().named['nn'])

    def test_visit_ImportFrom(self):
        test_code1 = 'from torch import *'
        test_code2 = 'from numpy import *'
        test_code3 = 'from torch import randn, Tensor'
        test_code4 = 'from math import sin'
        test_code5 = 'from torch.nn import x'

        # get souce structure depending on torch or sklearn selected
        with open('resultsPytorch.txt') as json_file:
            json_obj = json.load(json_file)
        source = json.loads(json_obj)

        imp = ImportVisitor('torch', source)

        tree = ast.parse(test_code1)
        imp.visit(tree)
        self.assertIn('torch', imp.get_imports().unknown)
        imp.del_imports()

        tree = ast.parse(test_code2)
        imp.visit(tree)
        self.assertNotIn('numpy', imp.get_imports().unknown)
        imp.del_imports()

        tree = ast.parse(test_code3)
        imp.visit(tree)
        self.assertIn('randn', imp.get_imports().named)
        self.assertIn('torch.randn', imp.get_imports().named['randn'])
        self.assertIn('Tensor', imp.get_imports().named)
        self.assertIn('torch.Tensor', imp.get_imports().named['Tensor'])
        imp.del_imports()

        tree = ast.parse(test_code4)
        imp.visit(tree)
        self.assertNotIn('math', imp.get_imports().named)
        self.assertNotIn('sin', imp.get_imports().named)
        imp.del_imports()

        tree = ast.parse(test_code5)
        imp.visit(tree)
        self.assertIn('x', imp.get_imports().named)
        self.assertIn('torch.nn.x', imp.get_imports().named['x'])
        imp.del_imports()
