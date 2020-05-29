"""
the here included function 'parse_code' combines all of the python files to first
visit the user code 'file' for imports, then variables, then functions and methods
"""

import json
import ast
import sys

import sklearn
import torch

from library import package_parser, struktur_implementation
from user_code.import_parser import ImportVisitor
from user_code.variable_parser import VariableVisitor
from user_code.code_parser import FunctionVisitor


def parse_code(file, module):
    # open file
    f = open(file, mode='r')
    contents = f.read()
    tree = ast.parse(contents)

    # decide for which module the code should be inspected
    source_file = ''
    if module == 'torch':
        source_file = 'library/results_torch.txt'

    elif module == 'sklearn':
        source_file = 'library/results_sklearn.txt'

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
    if len(sys.argv) == 3:
        file_path = sys.argv[1]
        bib = sys.argv[2]

        if (bib == 'torch') or (bib == 'sklearn'):
            # parse library
            package_parser.parse_package(bib)

            # parse code
            parse_code(file_path, bib)

        else:
            print('your libray is not supported. choose between pytorch and scikit')

    else:
        print('programm expects two arguments. firstly the destination path and secondly the library to check for.')

