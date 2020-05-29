"""
the here included function 'parse_code' combines all of the python files to first
visit the user code 'file' for imports, then variables, then functions and methods
"""

import json
import ast

from import_parser import ImportVisitor
from variable_parser import VariableVisitor
from code_parser import FunctionVisitor


def parse_code(file, module):
    # open file
    f = open(file, mode='r')
    contents = f.read()
    tree = ast.parse(contents)

    # decide for which module the code should be inspected
    source_file = ''
    if module == 'torch':
        source_file = 'resultsPytorch.txt'

    elif module == 'sklearn':
        source_file = 'resultsSKlearn.txt'

    # if none of the two is selected stop function
    else:
        return False

    # get souce structure depending on torch or sklearn selected
    with open(source_file) as json_file:
        json_obj = json.load(json_file)
    source = json.loads(json_obj)

    # get imports
    imp = ImportVisitor(module, source)
    imp.visit(tree)
    imps = imp.get_imports()

    # get vars
    var = VariableVisitor(imps)
    var.visit(tree)
    vars = var.get_vars()

    # inspect functions
    fp = FunctionVisitor(source, imps, vars)
    fp.visit(tree)


if __name__ == '__main__':
    parse_code('example.py', 'torch')

