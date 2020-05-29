import unittest
import json
import ast

from variables import UsedVariables
from imports import Imports
from variable_parser import VariableVisitor


class VariablesCase(unittest.TestCase):
    def test_get_var_type(self):
        uv = UsedVariables()
        uv.add_variable('var')
        uv.add_usage('var', 1, 'string')
        uv.add_usage('var', 3, 'int')
        uv.add_usage('var', 5, 'string')
        self.assertEqual(uv.get_var_type('var', 2), 'string', 'get_var_type does not iterate to far')
        self.assertEqual(uv.get_var_type('var', 4), 'int', 'get_var_type gets latest')

    def test_variable_parser_visit_annassign(self):
        # example code for testing
        code = 'a: x.cls1 = 1\nb: cls2 = 1\nc: cls3 = 1\nd: y.cls4 = 1\ne = 1'
        tree = ast.parse(code)

        # get imports
        imp = Imports()
        imp.add_named_import(package='xx', asname='x', line=0)
        imp.add_named_import(package='xx.cls2', asname='cls2', line=0)
        imp.add_unnamed_import(package='z', line=0)
        imp.set_package_content('z', ['cls3'])

        # parse with var_parser
        vv = VariableVisitor(imp)
        vv.visit(tree)
        vars = vv.get_vars()

        # if the type annotation has a prefix
        self.assertDictEqual(vars.dict['a'], {1: 'x.cls1'})
        # if the constructor is the prefix
        self.assertDictEqual(vars.dict['b'], {2: 'cls2'})
        # if constructor imported with *
        self.assertIn('c', vars.dict)               # make sure how to test this exactly
        # variable not belonging to module not added
        self.assertNotIn('d', vars.dict)
        # variable without type annotation ignored
        self.assertNotIn('e', vars.dict)


if __name__ == '__main__':
    unittest.main()
