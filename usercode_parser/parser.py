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




if __name__ == '__main__':
    # main for testing
    # will be rewritten for outside calls to a function
    # returns
    #   None: no relevant modules included
    #   Dict: else
    file = open('example.py', mode ='r')
    contents = file.read()

    tree = ast.parse(contents)

    if find_module('torch', tree):
        print('pytorch wurde in der Datei importiert.')
    else:
        print('pytorch wurde in der Datei nicht importiert.')
