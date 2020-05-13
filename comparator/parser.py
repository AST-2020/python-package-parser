import ast as ast
from typing import Any

class ImportVisitor(ast.NodeVisitor):
    # to get imported modules
    modules = []

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            self.modules.append(alias.name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        self.modules.append(node.module)

    def get_list(self, tree):
        # returns a list with all imported modules
        self.visit(tree)
        return self.modules


def find_module(name, tree):
    # checks if relvant module is included
    modules = ImportVisitor().get_list(tree)
    print(modules)
    if name in modules:
        return True
    return False

class NamedArg:
    # stores name and line of named arguments
    # line is needed for possible future output of error message
    def __init__(self, name, line):
        self.name = name
        self.line = line

    def get_name(self):
        return self.name

    def get_line(self):
        return self.line

class FunctionVisitor(ast.NodeVisitor):
    # gets all function calls and finds function name, named args, and code line
    # missing: package-path, real name, check for relevancy of function
    def visit_Call(self, node: ast.Call) -> Any:
        name = self.get_name(node)
        keywords = self.get_keywords(node)
        line = node.lineno
        path = ''
        # have to findout how to get the package path
        print('FUNCTION CALL::: in line ', line, ' of function ', name, ' with named args ', keywords)


    def get_name(self, node):
        name = node.func.value.id
        name += '.' + node.func.attr
        return name

    def get_keywords(self, node):
        list = []
        for keyword in node.keywords:
            list.append(keyword.arg)
        return list


if __name__ == '__main__':
    # main for testing
    # will be rewritten for outside calls to a function
    # returns
    #   None: no relevant modules included
    #   Dict: else
    file = open('test_dir/custom_test.py', mode ='r')
    contents = file.read()

    tree = ast.parse(contents)
    #print(ast.dump(tree))

    """
    if find_module('numpy', tree):
        print('pytorch wurde in der Datei importiert.')
    else:
        print('pytorch wurde in der Datei nicht importiert.')
    """

    FunctionVisitor().visit(tree)
