import ast
from collections import OrderedDict
from typing import Any, Dict


# differences:
# 1- lr_scheduler.pyi(in file: (scale_fn): Optional[Callable[[float], float]] vs
#       from code: Optional[Callable[float, float]])
# 2- opimizer.pyi (in file: (step): Optional[Callable[[], float]] vs
#         from code: Optional[Callable[, float]]

class _PythonPyiFileVisitor(ast.NodeVisitor):
    def __init__(self, function_name, searched_args: Dict, searched_cls_name=None):
        self.function_name = function_name
        self.searched_cls_name = searched_cls_name
        self.searched_args = searched_args
        self.single_type_hints = OrderedDict() # represent the type hints for a single occurence of function
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
                type_hint = self.find_inner_hint(arg.annotation)
                # print("the type hint", type_hint)
                self.single_type_hints[arg.arg] = type_hint

        # to test, if length of single_type_hints is equal to length of searched_args
        # if not, then the type hints belong to a different function
        if len(self.single_type_hints) != 0 and len(self.single_type_hints) == len(self.searched_args):
            self.returned_type_hints.append(self.single_type_hints)
            self.single_type_hints = OrderedDict()

    def find_inner_hint(self, subscriptable_object, hint_string=""):
        if subscriptable_object is None:
            return None
        if subscriptable_object.__dir__()[0] in ["id", "s"]:
            hint_string = getattr(subscriptable_object, subscriptable_object.__dir__()[0])
        elif subscriptable_object.__dir__()[0] == "value":
            hint = self.find_inner_hint(subscriptable_object.value)
            if hint is not None:
                hint_string += hint
            else:
                hint_string += "..."
        if "slice" in subscriptable_object.__dir__():
            hint_string += "[" + self.find_inner_hint(subscriptable_object.slice.value) + "]"
            # hint: Optional[Callable[, float]]
        elif subscriptable_object.__dir__()[0] in ["value", "id", "s"]:
            pass
        elif "elts" in subscriptable_object.__dir__():
            if len(subscriptable_object.elts) == 0:
                return "[]"
            for i in range(len(subscriptable_object.elts)):
                hint = self.find_inner_hint(subscriptable_object.elts[i])
                if i < len(subscriptable_object.elts) - 1:
                    if hint is not None:
                        hint_string += self.find_inner_hint(subscriptable_object.elts[i]) + ", "
                    else:
                        hint_string += "..., "
                else:
                    if hint is not None:
                        hint_string += self.find_inner_hint(subscriptable_object.elts[i])
                    else:
                        hint_string += "..."
        return hint_string

    def get_type_hints(self):
        if len(self.returned_type_hints) != 0:
            return self.returned_type_hints
        else:
            return None
