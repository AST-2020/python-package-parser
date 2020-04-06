import ast
from typing import Any


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.print_indented(f"------------ Start class: {node.name}  ------------")
        self.print_indented(f"Docstring:\n{ast.get_docstring(node)}")

        self.visit_children(node)
        self.print_indented(f"------------ End class: {node.name}  ------------")

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.print_indented(f"------------ Start function: {node.name}  ------------")
        self.print_indented(f"Docstring:\n{ast.get_docstring(node)}")
        self.print_indented(f"Arguments: {[arg.arg for arg in node.args.args]}")
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


if __name__ == '__main__':
    f = open("scikit-learn/SVC.py", mode="r")
    contents = f.read()

    tree = ast.parse(contents)
    MyNodeVisitor().visit(tree)
