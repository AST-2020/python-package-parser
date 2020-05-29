import ast
import os
from struktur_implementation import Structure
from typing import Any
import TestDirectory

# VIP: now we don't have self as parameter in method parameters
# this doesn't mean that the library is imported != from numpy import *
# this i not allowed --> import numpy.*
# import numpy


# to use file as main: uncomment: parse_package("torch") and  parse_package("sklearn")
# to run example in main: uncomment: parsed_data.convert_to_json("testTextFile") and enjoy ;)
# and to print any of the results refer to the (struktur_implementation.py) and uncomment what you want to print
#
# to use file as import: import the function (parse_package(package_name)) and input the name
# of the library you want to parse either (sklearn) or (torch)
# to parse both libraries, function must be used twice
#
# also refer to (struktur_implementation.py) for slight changes in structure


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

parsed_data = Structure()


def read_directory(directory, local_path, struct):
    for entry in os.scandir(directory):
        # we need (path) to have the path to the modules of the library on the device
        path = directory + "/" + entry.name
        # print(path)

        # (my_struct.module_path) is the path that will saved in the structure
        # and it represents the path, that we would get when we parse the imports in the user's code
        struct.module_path = path.replace("/", ".")
        struct.module_path = struct.module_path.replace(local_path, "")
        # print(struct.module_path)

        # in our implementation, we only parse files that end with .py
        if path.endswith(".py"):
            struct.module_path = struct.module_path.replace(".py", "")
            # had to ensure encoding is UTF-8 to avoid an error
            f = open(path, mode="r", encoding='utf-8')
            contents = f.read()
            tree = ast.parse(contents)
            MyNodeVisitor().visit(tree)

            struct.module_path = None
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
    global parsed_data
    parsed_data = Structure()
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
    indent = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        parsed_data.cls_name = node.name
        self.visit_children(node)
        # assign the name of the class to null after parsing the functions that are in that class
        parsed_data.cls_name = None

    # chose list to represent our arguments bec
    # 1. tuple can't be changed, so any performance gains (when adding) will be lost, when trying to add
    #   the defaults to the args_name
    # 2. a list would look more representable, because a tuple with only one value would look like (value1, )

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        args = [[arg.arg] for arg in node.args.args]
        # default_value_count represents how many default values we have
        # it represents the number of minimum arguments we have to enter
        default_value_count = len(args) - len(node.args.defaults)
        for default in node.args.defaults:
            default_attribute = default.__dir__()[0]
            args[default_value_count].append(getattr(default, default_attribute))
            default_value_count += 1

        if parsed_data.cls_name is None:
            parsed_data.add_func(parsed_data.module_path, node.name, args)
        else:
            args = args[1:]
            parsed_data.add_method(parsed_data.module_path, parsed_data.cls_name, node.name, args)
        # print(args)

    # to parse the import statements in the __init__.py in the package, if it exists
    # so that i can use it in visit_List
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if "__init__" not in parsed_data.module_path:
            return
        for obj in node.names:
            # print(node.module + "." + obj.name)
            if node.module is not None:
                parsed_data.import_list.append(node.module + "." + obj.name)
            else:
                parsed_data.import_list.append(obj.name)

    def visit_Import(self, node: ast.Import) -> Any:
        for obj in node.names:
            # print(obj.name)
            parsed_data.import_list.append(obj.name)

    # to test if the name of the variable is __all__ (variable is list in this case)
    def visit_Name(self, node: ast.Name):
        if node.id is "__all__":
            parsed_data.list__all__ = True

    # to parse the __all__ list in the __init__.py that is included in every packages, if it exists
    def visit_List(self, node: ast.List):
        if "__init__" not in parsed_data.module_path or not parsed_data.list__all__:
            return
        # to get all the names of the modules in the __all__ list
        modules = [obj.s for obj in node.elts]
        # to get the relative paths of the modules
        # if it is a fucntion or method we get its path using the list of imports we have from the
        # visit_ImportFrom method
        for i in range(len(modules)):
            for j in range(len(parsed_data.import_list)):
                # if we are importing a function or class, then the part after the import in (from .. import ..)
                # will be same as the name in the __all__ list
                if len(parsed_data.import_list[j].rsplit(".", 1)) == 2 and modules[i] == \
                        parsed_data.import_list[j].rsplit(".", 1)[1]:
                    modules[i] = parsed_data.import_list[j]
                    break

        # add the list of modules under the keys ['package__all__list']['the_package_name']
        parsed_data.add__all__(parsed_data.module_path.replace(".__init__", ""), modules)
        parsed_data.import_list = []
        parsed_data.list__all__ = False

    def print_indented(self, s):
        indentation = " " * self.indent
        for line in str(s).splitlines():
            print(indentation + line)

    def visit_children(self, node):
        self.indent += 2
        self.generic_visit(node)
        self.indent -= 2


if __name__ == '__main__':

    # will create a text file with parsed data for library Pytorch & sklearn
    # parse_package("torch")
    # parse_package("sklearn")

    # to create parsed data for TestDirectory
    library = TestDirectory.__file__
    library = library.replace("__init__.py", '')
    library = library[0:-1]
    path_to_delete = library.rsplit('TestDirectory', 1)[0]
    parsed_data = Structure()
    read_directory(library, path_to_delete, parsed_data)
    test_json_object = parsed_data.convert_to_json("TestDirectory")

    # to write our json data to a txt file
    # parsed_data.convert_to_python("results_testTextFile.txt")
