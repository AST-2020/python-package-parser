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

    # get souce structure
    source_file = ''
    if module == 'torch':
        source_file = 'resultsPytorch.txt'
    elif module == 'sklearn':
        source_file = 'resultsSKlearn.txt'

    with open(source_file) as json_file:
        json_obj = json.load(json_file)
    source = json.loads(json_obj)

    # print(source['method']['Tensor'])

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

