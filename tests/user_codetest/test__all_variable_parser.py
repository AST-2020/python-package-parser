
import unittest
import ast
from user_code.parser import AllVariableVisitor

class AllVariableCase(unittest.TestCase):

    @staticmethod
    def convert_vars_to_List(vars):
        tuple = [(var.name, var.value, var.type) for var in vars]
        return tuple

    def test_all_variable_parser_visit_assign(self):


        exp_usedvars=[]
        exp_usedvars.append(('a', 4, type(4)))
        exp_usedvars.append(('b',True, type(True)))
        exp_usedvars.append(('c', 'str', type('str')))

        text = 'a = 4 \nb = True \nc = "str" '
        tree = ast.parse(text)
        pass
        vars = AllVariableVisitor()
        vars.visit(tree)
        usedvars = vars.get_usedvars()
        list_usedvars = AllVariableCase.convert_vars_to_List(usedvars)
        self.assertListEqual(list_usedvars, exp_usedvars)
if __name__ == '__main__':
    unittest.main()