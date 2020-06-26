import ast
from typing import Any
from src.user_code.model import Variable


class AllVariableVisitor(ast.NodeVisitor):

    def __init__(self):
        self.usedvars: [Variable] = []

    def visit_Assign(self, node: ast.Assign) -> Any:

        line = node.lineno
        names_list= []
        values_list= []
        var_type = None
        for node in ast.walk(node):
            if isinstance(node, ast.Name):
                names_list.append(node.id)
            if isinstance(node, ast.Assign):
                # print(ast.dump(node))
                # print(node.value)
                if isinstance(node.value, ast.Dict):
                    var_type = type({})
                node = node.value
                if isinstance(node, ast.Tuple):
                    len = node.elts.__len__()
                    x = 0
                    while x < len:
                        values_list.append(getattr(node.elts[x], node.elts[x].__dir__()[0]))
                        x = x+1
                else:
                    # print(getattr(node, node.__dir__()[0]))
                    values_list.append(getattr(node, node.__dir__()[0]))


        if values_list.__len__() == names_list.__len__():
            x = 0
            while x < names_list.__len__():
                var = Variable(names_list[x], line, values_list[x])
                if var_type is not None:
                    var.set_type(var_type)
                self.usedvars.append(var)
                x = x + 1

        return self.usedvars

if __name__ == '__main__':
    with open('..\..\example.py', mode='r') as f:
        contents = f.read()
        tree = ast.parse(contents)

    var = AllVariableVisitor()
    var.visit(tree)

    # for node in ast.walk(tree):
    #     if isinstance(node, ast.Assign):
    #         # print(ast.dump(node))
    #         var.visit(node)

    for var in var.usedvars:
        var.print_variable()
        
