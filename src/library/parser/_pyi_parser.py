import ast
from typing import Any, Dict


class _PythonPyiFileVisitor(ast.NodeVisitor):
    def __init__(self, function_name, searched_args: Dict, searched_cls_name=None):
        self.function_name = function_name
        self.searched_cls_name = searched_cls_name
        self.searched_args = searched_args
        self.single_type_hints = {}
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
                    self.single_type_hints = None
                    break
                if arg.annotation is not None and "id" in arg.annotation.__dir__():
                    self.single_type_hints[arg.arg] = arg.annotation.id

                elif arg.annotation is not None:
                    self.single_type_hints[arg.arg] = self.find_inner_hint(arg.annotation)

                else:
                    self.single_type_hints[arg.arg] = None

        if len(self.single_type_hints) is not 0:
            self.returned_type_hints.append(self.single_type_hints)
            self.single_type_hints = {}

    def find_inner_hint(self, subscriptable_object, hint_string=""):
        hint_string += subscriptable_object.value.id + "["
        if "elts" in subscriptable_object.slice.value.__dir__():
            for hint in subscriptable_object.slice.value.elts:
                if type(hint) is ast.Subscript:
                    hint_string += self.find_inner_hint(hint) + ", "
                else:
                    hint_string += hint.id + ", "
            hint_string = hint_string[:-2] + "]"
        elif "slice" in subscriptable_object.slice.value.__dir__():
            hint_string += self.find_inner_hint(subscriptable_object.slice.value) + ", "
            hint_string = hint_string[:-2] + "]"
        else:
            hint_string += subscriptable_object.slice.value.id + "]"
        return hint_string

    def get_type_hints(self):
        if len(self.returned_type_hints) is not 0:
            return self.returned_type_hints
        else:
            return None