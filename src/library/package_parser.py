import ast
import os
from typing import Any, Optional, List, Dict
#from parse_pyi_file import MyPiFileNodeVisitor
from src.library.library_model import Library, Module, Class, Function, Parameter

# new limitations(example):
# 1- type hints from functions that are defined outside the class (example (defined in "autograd" i think ))
# torch\autograd\__init__.pyi
#
# 2- function Overload is not supported
# torch/__init__.pyi


# VIP: now we don't have "self" as parameter in method parameters
#
# to use file as main: uncomment: parse_package("torch") and  parse_package("sklearn")
# to run example in main: uncomment: parsed_data.convert_to_json("testTextFile") and enjoy ;)
#
# to use file as import: import the function (parse_package(package_name)) and input the name
# of the library you want to parse either (sklearn) or (torch)
# to parse both libraries, function must be used twice


try:
    import sklearn
except ModuleNotFoundError:
    sklearn_installed = False
else:
    sklearn_installed = True

# to test if the (torch) package is installed on the user's device, if not, then a warning will be issued
try:
    import torch
except ModuleNotFoundError:
    torch_installed = False
else:
    torch_installed = True


def read_directory(directory, local_path, struct: Library):
    for entry in os.scandir(directory):
        # we need (path) to have the path to the modules of the library on the device
        path = directory + "/" + entry.name
        # (my_struct.module_path) is the path that will saved in the structure
        # and it represents the path, that we would get when we parse the imports in the user's code

        # in our implementation, we only parse files that end with .py
        if path.endswith(".py") or path.endswith(".pyi"):
            parsed_pi_file = None
            module_path = path \
                .replace("/", ".") \
                .replace(local_path, "") \
                .replace(".py", "")
            if entry.name.replace(".py", ".pyi") in os.listdir(directory):
                f = open(path.replace(".py", ".pyi"), mode="r", encoding='utf-8')
                contents = f.read()
                tree = ast.parse(contents)
                parsed_pi_file = MyPiFileNodeVisitor(path)
                parsed_pi_file.visit(tree)

            current_module = Module(module_path, [], [])
            # had to ensure encoding is UTF-8 to avoid an error
            f = open(path, mode="r", encoding='utf-8')
            contents = f.read()
            tree = ast.parse(contents)
            # if parsed_pi_file is not None:
            #     MyNodeVisitor(current_module, pyi_file=parsed_pi_file.get_structure()).visit(tree)
            # else:
            MyNodeVisitor(current_module)

            struct.add_module(current_module)

        elif not entry.name.startswith('.') and entry.is_dir():
            read_directory(path, local_path, struct)


def has_package_installed(package_name):
    if package_name is "torch":
        if torch_installed:
            return True
        else:
            print("Warning: Pytorch library is not installed on your device")
            print("if you have installed this plugin to use with Pytorch, make sure you install the library first "
                  "and then run the program again")
            return False
    if sklearn_installed:
        return True
    else:
        print("warning: sklearn library is not installed on your device")
        print("if you have installed this plugin to use with Sci-Kit-learn, make sure you install the library first"
              " and then run the program again")
        return False


def parse_package(package_name):
    parsed_data = Library([])
    # package_name = torch or sklearn
    if not has_package_installed(package_name):
        return
    if package_name is "torch":
        library_local_path = torch.__file__
    elif package_name is "sklearn":
        library_local_path = sklearn.__file__
    library_local_path = library_local_path.replace("__init__.py", '')
    library_local_path = library_local_path[0:-1]

    # (local_path_to_delete) needed to access functions and methods from the local library
    # but will not be saved in the parsed data files
    local_path_to_delete = library_local_path.rsplit(package_name, 1)[0].replace("/", ".")

    read_directory(library_local_path, local_path_to_delete, parsed_data)
    parsed_data.convert_to_json(package_name)


class MyNodeVisitor(ast.NodeVisitor):
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
        for decorator in node.decorator_list:
            if "id" in decorator.__dir__() and decorator.id is "property":
                return
        parameters = self.__create_parameter_list(node)

        if self.__current_class is None:
            function = Function(node.name, parameters)
            self.__current_module.add_top_level_function(function)
        else:
            parameters = parameters[1:]
            function = Function(node.name, parameters)
            self.__current_class.add_method(function)

    def __create_parameter_list(self, node: ast.FunctionDef) -> List[Parameter]:
        param_name_and_hint = {}
        found_hint_in_definition = False
        for arg in node.args.args:
            if arg.annotation is not None:
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
            # call find_paramter_hint_in_doc_string()

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


if __name__ == '__main__':
    # will create a text file with parsed data for library Pytorch & sklearn
    parse_package("torch")
    parse_package("sklearn")

    # to create parsed data for TestDirectory
    # library = TestDirectory.__file__
    # library = library.replace("__init__.py", '')
    # library = library[0:-1]
    # path_to_delete = library.rsplit('TestDirectory', 1)[0]
    # parsed_data = Library([])
    # read_directory(library, path_to_delete, parsed_data)
    # test_json_object = parsed_data.convert_to_json("TestDirectory")

    # to write our json data to a txt file
    # parsed_data.convert_to_python("results_testTextFile.txt")
