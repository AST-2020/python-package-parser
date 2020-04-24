import ast
from typing import Any
from dict import *


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    def __init__(self):
        self.dict = Dict()
        self.classname = ''

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.print_indented(f"------------ Start class: {node.name}  ------------")
        self.print_indented(f"Docstring:\n{ast.get_docstring(node)}")
        # memorize current class and add to dict
        self.classname = node.name
        self.dict.addClass(self.classname)

        self.visit_children(node)
        self.print_indented(f"------------ End class: {node.name}  ------------")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.print_indented(f"------------ Start function: {node.name}  ------------")
        # add function of class to dict
        self.dict.addFunction(node.name, self.classname)

        self.print_indented(f"Docstring:\n{ast.get_docstring(node)}")

        self.print_indented(f"Arguments: {[arg.arg for arg in node.args.args]}")

        # add params to function of class to dict
        args = [arg.arg for arg in node.args.args]
        for arg in args:
            self.dict.addParam2Function(arg, node.name, self.classname)

        self.print_indented(f"Returns: {node.returns}")

        # We are currently not interested in the body of the function
        # self.visitChildren(node)
        self.print_indented(f"------------ End function: {node.name}  ------------")

    def print_indented(self, s):
        indentation = " " * self.indent
        for line in str(s).splitlines():
            print(indentation + line)

    def visit_children(self, node):
        self.indent += 2
        self.generic_visit(node)
        self.indent -= 2

    def getDict(self):
        return self.dict



if __name__ == '__main__':
    f = open("SVC.py", mode="r")
    contents = f.read()

    tree = ast.parse(contents)
    visitor = MyNodeVisitor()
    visitor.visit(tree)
    
    # get dict and print it out
    dict = visitor.getDict()
    print(dict.classes)


