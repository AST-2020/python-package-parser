import ast
from typing import Any
from user_code.model import Variable


class AllVariableVisitor(ast.NodeVisitor):

    def __init__(self):
        self.usedvars: [Variable] = []

    def visit_Assign(self, node: ast.Assign) -> Any:
        # # print(ast.dump(node))
        # len = node.targets[0].elts.__len__()
        # # print(len)
        # if len >1:
        #     x = 0
        #     while x < len:
        #         name = node.targets[0].elts[x].id
        #         self.l += self.l
        #         value = node.value.elts[x].n
        #         line = node.lineno
        #         print(len, name, value, line)
        #         self.vars.append((name, value, line))
        #         x = x+1
        #         # print(x)
        #
        # print( node.lineno)
        line = node.lineno
        names_list= []
        values_list= []
        for node in ast.walk(node):
            # print(ast.dump(node))
            if isinstance(node, ast.Name):
                # print(ast.dump(node))
                # print(node.id)
                names_list.append(node.id)
            if isinstance(node, ast.Assign):
                node = node.value

                # print(ast.dump(node))
                if isinstance(node, ast.Tuple):
                    len = node.elts.__len__()
                    x = 0
                    while x < len:
                        # print(getattr(node.elts[x], node.elts[x].__dir__()[0]))
                        # print(node.elts[x].__dir__()[0])
                        # print(ast.dump(node))
                        values_list.append(getattr(node.elts[x], node.elts[x].__dir__()[0]))
                        x = x+1
                else:
                    # print(getattr(node, node.__dir__()[0]))
                    values_list.append(getattr(node, node.__dir__()[0]))

        # print(names_list)
        # print(values_list)
        if values_list.__len__() == names_list.__len__():
            x = 0
            while x < names_list.__len__():
                var = Variable(names_list[x], line, values_list[x])
                self.usedvars.append(var)
                x = x + 1
        # print(self.usedvars)
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