import ast
from typing import Dict, Optional, Any, List

from src.library.model import Module
from ._pyi_parser import _PythonPyiFileVisitor
from collections import OrderedDict
from src.library.convert_string_to_type import convert_string_to_type
from src.library.model import Class, Function, Module, Parameter
from src.library.parser._docstring_parser import _find_parameter_hint_in_doc_string
from src.library.parser.utils import find_type_hint


def parse_module(module_path: str, python_file: str, python_interface_file: str) -> Module:
    """
    :param module_path: path of file found in the package, starting from the package name till the name of the module
        ex: "torch.optim.adam",

    :param python_file: local path of the module from the user device
        ex: "C:/Anaconda/envs/ml/lib/site-packages/torch/optim/adam.py",

    :param python_interface_file: similar to python_file, but gives the path for the pyi file when avalilable
        ex: "C:/Anaconda/envs/ml/lib/site-packages/torch/optim/adam.pyi"

    """
    if python_interface_file is not None:
        pyi_tree = _parse_python_interface_file(python_interface_file)  # generate the tree for the interface file
    else:
        pyi_tree = None

    module = Module(module_path)  # initialise a module obj with the module path as the name

    _parse_python_file(module, python_file, pyi_tree)
    return module


def _parse_python_file(module: Module, python_file: str, pyi_file_tree):
    with open(python_file, mode="r", encoding='utf-8') as f:
        contents = f.read()
        tree = ast.parse(contents)

        # generate an instance from the _PythonFileVisitor, which will parse the data saved
        # in the tree variable (the data from the python file)
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
            # property is a type of decorators that allows us to have two methods with the same name, while the one used
            # as the decorator not directly used by the user, as a result we don't need to include it in the structure
            if "id" in decorator.__dir__() and decorator.id == "property":
                return
        parameters = self.__find_properties_about_func(node)

        self.__create_fucntion_objects(node.name, self.__current_class, parameters)

    def __find_properties_about_func(self, node: ast.FunctionDef) -> List[List[Parameter]]:
        # variable, where we can save multiple (name_and_hint_dict) insatnces in case of overloaded functions or methods
        list_of_multiple_name_and_hint_dict = []

        # dict that saves the type hints for one function or method declaration with name
        name_and_hint_dict = OrderedDict()

        found_hint_in_definition = False  # boolean that allows to stop the search for the type_hint, once one is found
        for arg in node.args.args:
            type_hint = find_type_hint(arg.annotation)  # find type_hint from py files, if availble
            name_and_hint_dict[arg.arg] = None
            if type_hint is not None:
                type_hint = convert_string_to_type(type_hint)  # convert type_hint to wanted format, if found
                name_and_hint_dict[arg.arg] = type_hint  # add the type_hint for the param to the ordered dict
                found_hint_in_definition = True

        list_of_multiple_name_and_hint_dict.append(name_and_hint_dict)

        #  search for the type_hint, in the pyi_file, if available
        if not found_hint_in_definition and self.__pyi_file is not None:
            if self.__current_class is not None:
                pyi_type_hints = _PythonPyiFileVisitor(node.name, name_and_hint_dict,
                                                       self.__current_class.get_name())
            else:
                pyi_type_hints = _PythonPyiFileVisitor(node.name, name_and_hint_dict)

            # start parsing the tree of the pyi file, that we saved in the (parse_module) method
            pyi_type_hints.visit(self.__pyi_file)
            if pyi_type_hints.get_type_hints() is not None:
                # if the returned type_hints are not none, then we stop the search and get the type_hints back
                found_hint_in_definition = True
                list_of_multiple_name_and_hint_dict = pyi_type_hints.get_type_hints()

        if not found_hint_in_definition:
            doc_string = ast.get_docstring(node)  # get the doc_string from the func_body
            param_names = [n for n in name_and_hint_dict.keys()]

            # extract relevant data from the doc_string
            found_hints = _find_parameter_hint_in_doc_string(param_names, doc_string)
            if found_hints is not None:
                list_of_multiple_name_and_hint_dict = _find_parameter_hint_in_doc_string(param_names, doc_string)

        # find the default values for the function
        parameter_defaults: List[Any] = self.find_default_values(node)
        if list_of_multiple_name_and_hint_dict is None:
            return []
        else:
            return self.__create_parameter_objects(list_of_multiple_name_and_hint_dict, parameter_defaults)

    def find_default_values(self, node: ast.FunctionDef):
        return [getattr(default, default.__dir__()[0]) for default in node.args.defaults]

    def __create_parameter_objects(self, hints: List[Dict], defaults: List) -> List[List[Parameter]]:
        """
        the method couples the function/method name with its default value and type hints, and instantiates a parameter
        object for them

        :param hints: a list of dictionaries, one dictionary in case of non overloaded functions,
         that has the type hints for the function

        :param defaults: list of the default values for the parameters of the function
        """
        result = []  # saves all the occurrences of a a particular method/function
        one_function_param = []  # saves the parameter objects of one occurrence of the method/fucntion
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

    def __create_fucntion_objects(self, func_name, klass, parameters_for_all_occurences):
        if klass is None:
            if len(parameters_for_all_occurences) == 0:
                function = Function(func_name, [])
                self.__current_module.add_top_level_function(function)
            else:
                for params_of_one_instance in parameters_for_all_occurences:
                    function = Function(func_name, params_of_one_instance)
                    self.__current_module.add_top_level_function(function)
        else:
            if len(parameters_for_all_occurences) == 0:
                function = Function(func_name, [])
                klass.add_method(function)
            else:
                for params_of_one_instance in parameters_for_all_occurences:
                    if params_of_one_instance is not None:
                        params_of_one_instance = params_of_one_instance[1:]
                    function = Function(func_name, params_of_one_instance)
                    klass.add_method(function)
