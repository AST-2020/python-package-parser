import ast
from collections import OrderedDict
from typing import Any, Dict
from src.library.convert_string_to_type import convert_string_to_type
from src.library.parser.utils import find_type_hint


class _PythonPyiFileVisitor(ast.NodeVisitor):
    def __init__(self, function_name, searched_args: OrderedDict, searched_cls_name=None):
        self.function_name = function_name
        self.searched_cls_name = searched_cls_name
        self.searched_args = searched_args
        self.single_type_hints = OrderedDict()  # represent the type hints for a single occurence of function
        # list that represent all occurences of the function in the Module (multiple in case of overloaded functions)
        self.returned_type_hints = []
        self.cls_name = None

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        # to check if the class name we are searching
        self.cls_name = node.name
        if self.cls_name == self.searched_cls_name:
            self.generic_visit(node)
        self.cls_name = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        if node.name == self.function_name and self.cls_name == self.searched_cls_name:
            for arg in node.args.args:
                if arg.arg not in self.searched_args:
                    self.single_type_hints = OrderedDict()
                    break
                type_hint = find_type_hint(arg.annotation)
                if type_hint is not None:
                    type_hint = convert_string_to_type(type_hint)

                # print("the type hint", type_hint)
                self.single_type_hints[arg.arg] = type_hint

        # to test, if length of single_type_hints is equal to length of searched_args
        # if not, then the type hints belong to a different function
        if len(self.single_type_hints) != 0 and len(self.single_type_hints) == len(self.searched_args):
            self.returned_type_hints.append(self.single_type_hints)
            self.single_type_hints = OrderedDict()

    def get_type_hints(self):
        if len(self.returned_type_hints) != 0:
            return self.returned_type_hints
        else:
            return None
