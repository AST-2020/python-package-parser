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
                    self.single_type_hints = {}
                    break
                type_hint = self.find_inner_hint(arg.annotation)
                print("the type hint" ,type_hint)
                self.single_type_hints[arg.arg] = type_hint

        if len(self.single_type_hints) is not 0 and len(self.single_type_hints) == len(self.searched_args):
            self.returned_type_hints.append(self.single_type_hints)
            self.single_type_hints = {}

    def find_inner_hint(self, subscriptable_object, hint_string=""):
        if subscriptable_object is None:
            return None
        if subscriptable_object.__dir__()[0] in ["id", "s"]:
            hint_string = getattr(subscriptable_object, subscriptable_object.__dir__()[0])
        elif subscriptable_object.__dir__()[0] is "value":
            hint = self.find_inner_hint(subscriptable_object.value)
            if hint is not None:
                hint_string += hint
            else:
                hint_string += "..."
        if "slice" in subscriptable_object.__dir__():
            hint_string += "[" + self.find_inner_hint(subscriptable_object.slice.value) + "]"
        elif subscriptable_object.__dir__()[0] in ["value", "id", "s"]:
            pass
        elif "elts" in subscriptable_object.__dir__():
            for i in range(len(subscriptable_object.elts)):
                hint = self.find_inner_hint(subscriptable_object.elts[i])
                if i < len(subscriptable_object.elts)-1:
                    if hint is not None:
                        hint_string += self.find_inner_hint(subscriptable_object.elts[i]) + ", "
                    else:
                        hint_string += "..., "
                else:
                    if hint is not None:
                        hint_string += self.find_inner_hint(subscriptable_object.elts[i])
                    else:
                        hint_string += "..."
        else:
            print("searched for", subscriptable_object.__dir__())
        return hint_string

    def get_type_hints(self):
        if len(self.returned_type_hints) is not 0:
            return self.returned_type_hints
        else:
            return None