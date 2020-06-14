import json
import ast
import unittest

from user_code.model import Imports
from user_code.parser._import_parser import ImportVisitor


class ImportParserTestCase(unittest.TestCase):
    """
    def test_get_package_from_content(self):
        imp = Imports()
        imp.add_unnamed_import('x', 1)
        imp.set_package_content('x', ['a'])

        # check if package is found for content
        self.assertEqual('x', imp.get_package_from_content('a',2))
        # check if not inclouded name returns None
        self.assertIs(imp.get_package_from_content('b',2), None)
    """

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
        self.assertIn('torch', imp.imports.imports)
        self.assertIn('torch', imp.imports.imports['torch'])
        imp.imports = Imports()

        tree = ast.parse(test_code2)
        imp.visit(tree)
        self.assertIn('t', imp.imports.imports)
        self.assertIn('torch', imp.imports.imports['t'])
        imp.imports = Imports()

        tree = ast.parse(test_code3)
        imp.visit(tree)
        self.assertIn('t', imp.imports.imports)
        self.assertIn('torch', imp.imports.imports['t'])
        self.assertNotIn('np', imp.imports.imports)
        self.assertNotIn('numpy', imp.imports.imports)
        imp.imports = Imports()

        tree = ast.parse(test_code4)
        imp.visit(tree)
        self.assertIn('nn', imp.imports.imports)
        self.assertIn('torch.nn', imp.imports.imports['nn'])
        imp.imports = Imports()

        tree = ast.parse(test_code5)
        imp.visit(tree)
        self.assertIn('nn', imp.imports.imports)
        self.assertIn('torch.nn', imp.imports.imports['nn'])

    def test_visit_ImportFrom(self):
        test_code3 = 'from torch import randn, Tensor'
        test_code4 = 'from math import sin'
        test_code5 = 'from torch.nn import x'

        # get souce structure depending on torch or sklearn selected
        with open('resultsPytorch.txt') as json_file:
            json_obj = json.load(json_file)
        source = json.loads(json_obj)

        imp = ImportVisitor('torch', source)

        tree = ast.parse(test_code3)
        imp.visit(tree)
        self.assertIn('randn', imp.imports.imports)
        self.assertIn('torch.randn', imp.imports.imports['randn'])
        self.assertIn('Tensor', imp.imports.imports)
        self.assertIn('torch.Tensor', imp.imports.imports['Tensor'])
        imp.imports = Imports()

        tree = ast.parse(test_code4)
        imp.visit(tree)
        self.assertNotIn('math', imp.imports.imports)
        self.assertNotIn('sin', imp.imports.imports)
        imp.imports = Imports()

        tree = ast.parse(test_code5)
        imp.visit(tree)
        self.assertIn('x', imp.imports.imports)
        self.assertIn('torch.nn.x', imp.imports.imports['x'])
        imp.imports = Imports()
