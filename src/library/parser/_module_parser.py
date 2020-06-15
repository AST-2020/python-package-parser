import ast
from typing import Dict, Optional, Any, List

from library.model import Class, Function, Module, Parameter
from ._pyi_parser import _PythonPyiFileVisitor


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
    def __init__(self, current_module: Module, pyi_file = None):
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
        parameters = self.__create_parameter_list(node)

        if self.__current_class is None:
            function = Function(node.name, parameters)
            self.__current_module.add_top_level_function(function)
        else:
            parameters = parameters[1:]
            function = Function(node.name, parameters)
            self.__current_class.add_method(function)

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

    def __create_parameter_list(self, node: ast.FunctionDef) -> List[Parameter]:
        param_name_and_hint = {}
        found_hint_in_definition = False
        for arg in node.args.args:
            if arg.annotation is not None and "id" in arg.annotation.__dir__():
                found_hint_in_definition = True
                param_name_and_hint[arg.arg] = arg.annotation.id

            elif arg.annotation is not None:
                pass
                # self.find_inner_hint(arg.annotation)

            # torch.testing._internal.distributed.rpc.jit.rpc_test
            # None
            # rpc_async_call_remote_torchscript_in_torchscript
            #
            # torch.testing._internal.distributed.rpc.jit.rpc_test
            # None
            # rpc_async_call_remote_torchscript_in_torchscript

            else:
                param_name_and_hint[arg.arg] = None

        if not found_hint_in_definition and self.__pyi_file is not None:
            if self.__current_class is not None:
                pyi_type_hints = _PythonPyiFileVisitor(node.name, param_name_and_hint, self.__current_class.get_name())
            else:
                pyi_type_hints = _PythonPyiFileVisitor(node.name, param_name_and_hint)
            pyi_type_hints.visit(self.__pyi_file)
            type_hints = pyi_type_hints.get_type_hints()
            if type_hints is not None:
                print(type_hints)


        if not found_hint_in_definition:
            doc_string = ast.get_docstring(node)
            # call find_paramter_hint_in_doc_string()

        # end format before entering the values in the structure --> List(tuple)
        param_name_and_hint = [(name, type) for name, type in param_name_and_hint.items()]

        parameter_defaults: List[Any] = [getattr(default, default.__dir__()[0]) for default in node.args.defaults]

        result: List[Parameter] = []
        for i in range(len(param_name_and_hint)):
            default_index = i + len(parameter_defaults) - len(param_name_and_hint)
            if default_index < 0:  # Parameter has no default value
                if len(param_name_and_hint[i]) == 1:
                    result.append(Parameter(param_name_and_hint[i][0]))
                else:
                    result.append(Parameter(param_name_and_hint[i][0], type_hint=param_name_and_hint[i][1]))
            else:
                if len(param_name_and_hint[i]) == 1:
                    result.append(Parameter(param_name_and_hint[i][0], True, parameter_defaults[default_index]))
                else:
                    result.append(Parameter(param_name_and_hint[i][0], type_hint=param_name_and_hint[i][1],
                                            has_default=True, default=parameter_defaults[default_index]))
        return result
