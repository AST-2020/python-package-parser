import ast
from typing import Any


class MyPiFileNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.__current_class = None
        self.__module_structure = {}

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.__current_class = node.name
        self.__module_structure[self.__current_class] = {}
        self.generic_visit(node)
        self.__current_class = None  # Exit the class scope

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        parameter_name_and_hint = []
        for arg in node.args.args:
            if arg.annotation is not None:
                parameter_name_and_hint.append((arg.arg, arg.annotation.id))
            else:
                parameter_name_and_hint.append((arg.arg,))
        if self.__current_class is None:
            self.__module_structure[node.name] = parameter_name_and_hint
        else:
            self.__module_structure[self.__current_class][node.name] = parameter_name_and_hint

    def get_structure(self):
        return self.__module_structure
