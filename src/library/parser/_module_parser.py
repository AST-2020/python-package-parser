import ast
from typing import Dict, Optional, Any, List

from src.library.model import Class, Function, Module, Parameter
from src.library.parser._docstring_parser import _find_parameter_hint_in_doc_string


def parse_module(module_path: str, python_file: str, python_interface_file: str) -> Module:
    module = Module(module_path)

    _parse_python_file(module, python_file)
    if python_interface_file is not None:
        _parse_python_interface_file(module, python_interface_file)

    return module


def _parse_python_file(module: Module, python_file: str):
    with open(python_file, mode="r", encoding='utf-8') as f:
        contents = f.read()
        tree = ast.parse(contents)
        _PythonFileVisitor(module).visit(tree)


def _parse_python_interface_file(module: Module, python_interface_file: str):
    with open(python_interface_file, mode="r", encoding='utf-8') as f:
        pass  # TODO

class _PythonFileVisitor(ast.NodeVisitor):
    def __init__(self, current_module: Module, pyi_file: Dict = None):
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
        if node.name == "device":
            print(self.__current_module, " ", self.__current_class)
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

    @staticmethod
    def __create_parameter_list(node: ast.FunctionDef) -> List[Parameter]:
        param_name_and_hint = {}
        found_hint_in_definition = False
        for arg in node.args.args:
            if arg.annotation is not None and "id" in arg.annotation.__dir__():
                found_hint_in_definition = True
                param_name_and_hint[arg.arg] = arg.annotation.id
            else:
                param_name_and_hint[arg.arg] = None

        # if not found_hint_in_definition and self.__pyi_file is not None:
        #     args_list = []
        #     if self.__current_class is not None and self.__current_class.get_name() in self.__pyi_file \
        #             and node.name in self.__pyi_file[self.__current_class.get_name()]:
        #         args_list = self.__pyi_file[self.__current_class.get_name()][node.name]
        #     elif node.name in self.__pyi_file:
        #         args_list = self.__pyi_file[node.name]
        #     for element in args_list:
        #         if len(element) is 1:
        #             param_name_and_hint[element[0]] = None
        #         else:
        #             param_name_and_hint[element[0]] = element[1]

        if not found_hint_in_definition:
            doc_string = ast.get_docstring(node)
            _find_parameter_hint_in_doc_string(doc_string)

        # end format before entering the values in the structure --> List(tuple)
        param_name_and_hint = [(name, type) for name, type in param_name_and_hint.items()]
        # print(node.name, "  ",param_name_and_hint)

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
