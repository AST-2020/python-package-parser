import ast
import os
from typing import Any, Optional, List

from experiments.new_structure.library_model import Library, Module, Class, Function, Parameter

import TestDirectory

# VIP: now we don't have self as parameter in method parameters


# to use file as main: uncomment: parse_package("torch") and  parse_package("sklearn")
# to run example in main: uncomment: parsed_data.convert_to_json("testTextFile") and enjoy ;)
# and to print any of the results refer to the (library_model.py) and uncomment what you want to print
#
# to use file as import: import the function (parse_package(package_name)) and input the name
# of the library you want to parse either (sklearn) or (torch)
# to parse both libraries, function must be used twice
#
# also refer to (library_model.py) for slight changes in structure


# to test if the (sklearn) package is installed on the user's device, if not, then a warning will be issued


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


# to have a better understanding  of the program a smaller Directory called "TestDirectory" has been created
# and the program was used to parse that directory and the results were saved in testTextFile.txt
# and to show we can retrieve data from  the structure refer to files ("import_parser.py" & "file_to_test")


def read_directory(directory, local_path, struct: Library):
    for entry in os.scandir(directory):
        # we need (path) to have the path to the modules of the library on the device
        path = directory + "/" + entry.name
        # print(path)

        # (my_struct.module_path) is the path that will saved in the structure
        # and it represents the path, that we would get when we parse the imports in the user's code

        # in our implementation, we only parse files that end with .py
        if path.endswith(".py"):
            module_path = path \
                .replace("/", ".") \
                .replace(local_path, "") \
                .replace(".py", "")
            current_module = Module(module_path, [], [])

            # had to ensure encoding is UTF-8 to avoid an error
            f = open(path, mode="r", encoding='utf-8')
            contents = f.read()
            tree = ast.parse(contents)
            MyNodeVisitor(current_module).visit(tree)

            struct.add_module(current_module)

        # if file is not a py file, then test if it's a directory, if so
        # then call the read_directory recursively on that directory passing its complete (path)
        elif not entry.name.startswith('.') and entry.is_dir():
            read_directory(path, local_path, struct)


def is_package_installed(package_name):
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
    if not is_package_installed(package_name):
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
    # print(local_path_to_delete)

    read_directory(library_local_path, local_path_to_delete, parsed_data)

    # to write our json data to a txt file
    parsed_data.convert_to_json(package_name)


class MyNodeVisitor(ast.NodeVisitor):
    __current_class: Optional[Class] = None

    def __init__(self, current_module: Module):
        self.__current_module = current_module

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.__current_class = Class(node.name, [])
        self.generic_visit(node)
        self.__current_module.add_class(self.__current_class)
        self.__current_class = None  # Exit the class scope

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        parameters = self.__create_parameter_list(node)
        function = Function(node.name, parameters)

        if self.__current_class is None:
            self.__current_module.add_top_level_function(function)
        else:
            self.__current_class.add_method(function)

    def __create_parameter_list(self, node: ast.FunctionDef) -> List[Parameter]:
        parameter_names: List[str] = [arg.arg for arg in node.args.args]
        parameter_defaults: List[Any] = [self.__get_default_value(default) for default in node.args.defaults]

        result: List[Parameter] = []
        for i in range(len(parameter_names)):
            default_index = i + len(parameter_defaults) - len(parameter_names)
            if default_index < 0:  # Parameter has no default value
                result.append(Parameter(parameter_names[i]))
            else:
                result.append(Parameter(parameter_names[i], True, parameter_defaults[default_index]))

        return result

    def __get_default_value(self, node: ast.AST) -> Any:
        return node.__dir__()[0]


if __name__ == '__main__':
    # will create a text file with parsed data for library Pytorch & sklearn
    # parse_package("torch")
    # parse_package("sklearn")

    # to create parsed data for TestDirectory
    library = TestDirectory.__file__
    library = library.replace("__init__.py", '')
    library = library[0:-1]
    path_to_delete = library.rsplit('TestDirectory', 1)[0]
    parsed_data = Library([])
    read_directory(library, path_to_delete, parsed_data)
    test_json_object = parsed_data.convert_to_json("TestDirectory")

    # to write our json data to a txt file
    # parsed_data.convert_to_python("results_testTextFile.txt")
