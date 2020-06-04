"""
the here included function 'parse_code' combines all of the python files to first
visit the user code 'file' for imports, then variables, then functions and methods
"""

import json
import ast
import sys

from library import library_model
from library.package_parser import parse_package

from user_code.import_parser import ImportVisitor
from user_code.variable_parser import VariableVisitor
from user_code.code_parser import FunctionVisitor


def parse_code(file, module):
    source_file_torch = 'library/results_torch.json'
    source_file_sklearn = 'library/results_sklearn.json'
    # open file
    f = open(file, mode='r')
    contents = f.read()
    tree = ast.parse(contents)

    # get souce structure depending on torch or sklearn selected
    source = library_model.Library([])
    if module == 'torch':
        source.convert_to_python(source_file_torch)
    else:
        source.convert_to_python(source_file_sklearn)

    # get imports
    imp = ImportVisitor(module, source)
    imp.visit(tree)
    imps = imp.get_imports()

    # get vars
    var = VariableVisitor(imps)
    var.visit(tree)
    vars = var.get_vars()

    # inspect functions
    fp = FunctionVisitor(file_path, source, imps, vars)
    fp.visit(tree)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]

        # parse torch and sklearn library
        parse_package('torch')
        # parse_package('sklearn')


        # parse code for both libraries
        parse_code(file_path, 'torch')
        # parse_code(file_path, 'sklearn')

    else:
        print('programm expects only the file to check as an argument.')

