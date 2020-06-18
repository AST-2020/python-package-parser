import ast
import re
from typing import Dict, Optional, Any, List

from library.model import Class, Function, Module, Parameter


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

def _find_parameter_hint_epy_style(doc_string):
    '''
    search epy text docstrings for parameters
    epy text examples:
    "@param(s) param_name: description"
    "@params param_name :description"
    '''
    expr = r'@\s?params?\s(.+?)\s?:\s*(.+?)\n+'
    params = re.compile(expr, re.MULTILINE)

    if doc_string is None:
        return None

    p = params.findall(doc_string)
    if p != []:
        print(p)
        return p
    return None

def _find_parameter_hint_google_style(doc_string):
    '''
    search NumpyDoc style docstrings for parameters
    This is an example of Google style.

    Args:
        param1: This is the first param.
        param2: This is a second param.

    Returns:
        This is a description of what is returned.

    Raises:
        KeyError: Raises an exception.
    '''
    param_section = None
    # used keywords to references sections within the docstings
    wanted_sections = ["Args", "Arg", "Paramter", "Param", "Parameters"]
    unwanted_sections = ['Returns', 'Notes', 'See also', 'Examples', 'References', 'Yields', 'Raises', 'Warns']
    # create regex compiler
    expr = r'^({}):?\n+'.format('|'.join(wanted_sections+unwanted_sections))
    sections = re.compile(expr, re.M|re.S)

    if doc_string is None:
        return None

    # isolate parameter section
    section = sections.split(doc_string)
    if section is not None:
        for i in range(len(section)):
            if section[i] in wanted_sections:
                param_section = section[i+1]

    # extract params
    if param_section is not None:
        expr = r'^\s+(.+?)\s(.+?)\n'
        params= re.compile(expr, re.M)
        return params.findall(param_section)

    return None

def _find_parameter_hint_numpydoc_style(doc_string):
    '''
    search NumpyDoc style docstrings for parameters
    example:
        "Parameter(s)
        --------------
        first : array_like
            the 1st param name `first`
        second :
            the 2nd param
        third : {'value', 'other'}, optional
            the 3rd param, by default 'value'"
    '''
    # --- isolate parameter section ---
    param_section = None
    # used keywords to references sections within the docstings
    keywords = ['Parameters', 'Parameter', 'Returns', 'Notes', 'See also', 'Examples', 'References', 'Yields', 'Raises',
                'Warns']
    # create regex compiler
    expr = r'[\n]*({})\n[-]+\n'.format('|'.join(keywords))
    sections = re.compile(expr, re.MULTILINE | re.S)

    # if doc_string is not empty, split by keywords in text sections
    if doc_string is None:
        return None

    splits = sections.split(doc_string)

    # das sortieren in ein dict muss doch auch schon direkt moeglich sein
    for i in range(len(splits)):
        if splits[i] in ['Parameters', 'Parameter']:
            # store found sections and contents in a dict
            param_section = splits[i + 1].strip('\n')

    # --- divide param_section in list of (param_name, type_info) touples---
    if param_section is not None:
        expr = r'\n*(.+?) : (.+?)[\n\t.+]+'
        params = re.compile(expr, re.MULTILINE)
        return params.findall(param_section)
    return None

def _find_parameter_hint_rest_style(doc_string):
    '''
    search reST style docstrings for parameters
    reSt style examples:
    ":param(s) param_name: description"
    ":params param_name :description"
    '''
    expr = r':\s?params?\s(.+?)\s?:\s*(.+?)\n+'
    params = re.compile(expr, re.MULTILINE)

    if doc_string is None:
        return None

    p = params.findall(doc_string)
    if p != []:
        return p
    return None

def _find_parameter_hint_in_doc_string(doc_string: str):
    # if numpydoc style
    if _find_parameter_hint_numpydoc_style(doc_string) is not None:
        pass
    # if reST doc style
    elif _find_parameter_hint_rest_style(doc_string) is not None:
        pass
    elif _find_parameter_hint_epy_style(doc_string):
        pass
    elif _find_parameter_hint_google_style(doc_string):
        pass

    # elif doc_string is not None:
    #     print(doc_string)

    pass

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
