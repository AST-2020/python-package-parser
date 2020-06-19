import ast
from typing import Dict, Optional, Any, List

from library.model import Class, Function, Module, Parameter
from ._pyi_parser import _PythonPyiFileVisitor
from collections import OrderedDict


# examples for special cases:
# torch.testing._internal.distributed.rpc.jit.rpc_test
# None
# rpc_async_call_remote_torchscript_in_torchscript
#
# torch.testing._internal.distributed.rpc.jit.rpc_test
# None
# rpc_async_call_remote_torchscript_in_torchscript


def parse_module(module_path: str, python_file: str, python_interface_file: str) -> Module:
    if python_interface_file is not None:
        tree = _parse_python_interface_file(python_interface_file)
    else:
        tree = None

    module = Module(module_path)

    _parse_python_file(module, python_file, tree)
    return module


def _parse_python_file(module: Module, python_file: str, pyi_file_tree):
    with open(python_file, mode="r", encoding='utf-8') as f:
        contents = f.read()
        tree = ast.parse(contents)
        _PythonFileVisitor(module, pyi_file=pyi_file_tree).visit(tree)


def _parse_python_interface_file(python_interface_file: str):
    with open(python_interface_file, mode="r", encoding='utf-8') as f:
        contents = f.read()
        tree = ast.parse(source=contents)
        return tree


class _PythonFileVisitor(ast.NodeVisitor):
    def __init__(self, current_module: Module, pyi_file=None):
        self.__current_module = current_module
        self.__pyi_file = pyi_file
        self.__current_class: Optional[Class] = None

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.__current_class = Class(node.name, [])
        self.generic_visit(node)
        if self.__current_class is not None:
            self.__current_module.add_class(self.__current_class)
        self.__current_class = None  # Exit the class scope

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        for decorator in node.decorator_list:
            if "id" in decorator.__dir__() and decorator.id == "property":
                return
        parameters = self.__create_parameter_lists(node)

        if self.__current_class is None:
            for param_obj in parameters:
                function = Function(node.name, param_obj)
                self.__current_module.add_top_level_function(function)
        else:
            for param_obj in parameters:
                if param_obj is not None:
                    param_obj = param_obj[1:]
                function = Function(node.name, param_obj)
                self.__current_class.add_method(function)

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
            # hint: Optional[Callable[, float]]
        elif subscriptable_object.__dir__()[0] in ["value", "id", "s"]:
            pass
        elif "elts" in subscriptable_object.__dir__():
            if len(subscriptable_object.elts) is 0:
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

    def __create_parameter_lists(self, node: ast.FunctionDef) -> List[Parameter]:
        param_name_and_hint = []
        name_and_hint_dict = {}
        found_hint_in_definition = False
        # for arg in node.args.args:
        #     if arg.annotation is not None and "id" in arg.annotation.__dir__():
        for arg in node.args.args:
            type_hint = self.find_inner_hint(arg.annotation)
            # print("the type hint", type_hint)
            name_and_hint_dict[arg.arg] = type_hint
            found_hint_in_definition = True

        # to test, if length of single_type_hints is equal to length of searched_args
        # if not, then the type hints belong to a different function
        param_name_and_hint.append(name_and_hint_dict)
        self.single_type_hints = OrderedDict()

        if not found_hint_in_definition and self.__pyi_file is not None:
            if self.__current_class is not None:
                pyi_type_hints = _PythonPyiFileVisitor(node.name, name_and_hint_dict, self.__current_class.get_name())
            else:
                pyi_type_hints = _PythonPyiFileVisitor(node.name, name_and_hint_dict)
            pyi_type_hints.visit(self.__pyi_file)
            param_name_and_hint = pyi_type_hints.get_type_hints()

        if not found_hint_in_definition:
            doc_string = ast.get_docstring(node)
            # call find_paramter_hint_in_doc_string()

        parameter_defaults: List[Any] = [getattr(default, default.__dir__()[0]) for default in node.args.defaults]
        if param_name_and_hint is None:
            return []
        else:
            return self.__create_parameter_objects(param_name_and_hint, parameter_defaults)

    def __create_parameter_objects(self, hints: List[Dict], defaults: List):
        result: List[Parameter] = []
        one_function_param = []
        for hint in hints:
            hint_as_list = [(name, type) for name, type in hint.items()]
            for i in range(len(hint_as_list)):
                default_index = i + len(defaults) - len(hint_as_list)
                if default_index < 0:  # Parameter has no default value
                    if hint_as_list[i][1] is None:
                        one_function_param.append(Parameter(hint_as_list[i][0]))
                    else:
                        one_function_param.append(Parameter(hint_as_list[i][0], type_hint=hint_as_list[i][1]))
                else:
                    if hint_as_list[i][1] is None:
                        one_function_param.append(
                            Parameter(hint_as_list[i][0], has_default=True, default=defaults[default_index]))
                    else:
                        one_function_param.append(Parameter(hint_as_list[i][0], type_hint=hint_as_list[i][1],
                                                            has_default=True, default=defaults[default_index]))
            result.append(one_function_param)
            one_function_param = []
        return result
