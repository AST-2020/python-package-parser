import ast
from typing import Any, Dict


class PyiModule:
    def __init__(self):
        self.__classes: Dict[str: PyiClass] = {}
        self.__top_level_functions: Dict[str: PyiFunction] = {}
        self.__to_ignore = []

    def add_Class(self, cls_name):
        self.__classes[cls_name] = PyiClass(cls_name)

    def add_Function(self, func_name):
        self.__top_level_functions[func_name] = PyiFunction(func_name)

class PyiClass:
    def __init__(self, cls_name):
        self.__cls_name = cls_name
        self.__top_level_functions: Dict[str: PyiFunction] = {}
        self.__to_ignore = []

    def add_Function(self, func_name):
        self.__top_level_functions[func_name] = PyiFunction(func_name)


class PyiFunction:
    def __init__(self, func_name):
        pass


class MyPiFileNodeVisitor(ast.NodeVisitor):
    def __init__(self, module_name):
        self.__current_class = None
        self.__methods_to_ignore =[]
        self.__classes_to_ignore = []
        self.__functions_to_ignore = []
        self.__module_structure = PyiModule()
        self.__module_name = module_name

    # def visit_ClassDef(self, node: ast.ClassDef) -> Any:
    #     self.__current_class = node.name
    #     if self.__current_class not in self.__module_structure and self.__current_class not in self.__classes_to_ignore:
    #         self.__module_structure[self.__current_class] = {}
    #     else:
    #         self.__module_structure.pop(self.__current_class, None)
    #         self.__classes_to_ignore.append(self.__current_class)
    #     self.generic_visit(node)
    #     self.__current_class = None  # Exit the class scope
    #
    # def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
    #     parameter_name_and_hint = []
    #     for arg in node.args.args:
    #         if arg.annotation is not None and "id" in arg.annotation.__dir__():
    #             parameter_name_and_hint.append((arg.arg, arg.annotation.id))
    #         else:
    #             parameter_name_and_hint.append((arg.arg,))
    #     if self.__current_class is None:
    #         if node.name not in self.__module_structure.keys():
    #             self.__module_structure[node.name] = parameter_name_and_hint
    #         else:
    #             del(self.__module_structure[node.name])
    #             self.__functions_to_ignore.append(node.name)
    #     else:
    #         if node.name not in self.__module_structure[self.__current_class].keys():
    #             self.__module_structure[self.__current_class][node.name] = parameter_name_and_hint
    #         else:
    #             del(self.__module_structure[self.__current_class][node.name])
    #             self.__methods_to_ignore.append(node.name)
    #
    # def get_structure(self):
    #     return self.__module_structure

    # def add_function(self, func_name, cls_name=None):
    #     if cls_name is None:

