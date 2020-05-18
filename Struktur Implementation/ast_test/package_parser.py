import ast
import json
import os
from struktur_implementation import Structure
from typing import Any
import TestDirectory

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


def read_directory(directory, local_path, struct):
    for entry in os.scandir(directory):
        # we need (path) to have the path to the modules of the library on the device
        path = directory + "/" + entry.name
        # print(path)

        # (my_struct.module_path) is the path that will saved in the structure
        # and it represents the path, that we would get when we parse the imports in the user's code
        struct.module_path = path.replace("/", ".")
        struct.module_path = struct.module_path.replace(local_path, "")
        # print(my_struct.module_path)

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


# to parse the torch package
def parse_torch():
    library_local_path = torch.__file__
    library_local_path = library_local_path.replace("__init__.py", '')
    # (local_path_to_delete) will be passed to further functions and methods
    # and this is the part of the path that we should delete
    local_path_to_delete = library_local_path.rsplit('torch', 1)[0]
    read_directory(library_local_path, local_path_to_delete, struct)
    torch_json_object = struct.toJSON()

    # to print our structure in JSON format
    # print(torch_json_object)

    # to write our json data to a txt file
    with open('resultsTorch.txt', 'w') as torch_outfile:
        json.dump(torch_json_object, torch_outfile)

    print("Package torch has been successfully parsed")


# to parse the sklearn package
def parse_sklearn():
    library_local_path = sklearn.__file__
    library_local_path = library_local_path.replace("__init__.py", '')
    # (local_path_to_delete) will be passed to further functions and methods
    # and this is the part of the path that we should delete
    local_path_to_delete = library_local_path.rsplit('sklearn', 1)[0]
    read_directory(library_local_path, local_path_to_delete, struct)
    sklearn_json_object = struct.toJSON()

    # to print our structure in JSON format
    # print(json_object)

    # to write our json data to a txt file
    with open('resultsSklearn.txt', 'w') as sklearn_outfile:
        json.dump(sklearn_json_object, sklearn_outfile)
    print("Package sklearn has been successfully parsed")


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:

        # my_struct.cls_name represents the name of our class
        struct.cls_name = node.name
        if struct.module_path not in struct.dict["method"]:
            struct.add_module_path("method", struct.module_path)
        struct.add_class_name(struct.module_path, struct.cls_name)
        self.visit_children(node)
        # assign the name of the class to null after parsing the functions that are in that class
        struct.cls_name = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        args = [arg.arg for arg in node.args.args]
        if struct.cls_name is None:
            if struct.module_path not in struct.dict["function"]:
                struct.add_module_path("function", struct.module_path)
            struct.add_func(struct.module_path, node.name, args)
        else:
            struct.add_method(struct.module_path, struct.cls_name, node.name, args)

    # to parse the import statements in the __init__.py in the package, if it exists
    # so that i can use it in visit_List
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if "__init__" not in struct.module_path:
            return
        for obj in node.names:
            # print(node.module + "." + obj.name)
            if node.module is not None:
                struct.import_list.append(node.module + "." + obj.name)
            else:
                struct.import_list.append(obj.name)

    def visit_Import(self, node: ast.Import) -> Any:
        for obj in node.names:
            # print(obj.name)
            struct.import_list.append(obj.name)

    # to test if the name of the variable is __all__ (variable is list in this case)
    def visit_Name(self, node: ast.Name):
        if node.id is "__all__":
            struct.list__all__ = True

    # to parse the __all__ list in the __init__.py that is included in every packages, if it exists
    def visit_List(self, node: ast.List):
        if "__init__" not in struct.module_path or not struct.list__all__:
            return
        # to get all the names of the modules in the __all__ list
        modules = [obj.s for obj in node.elts]
        # to get the relative paths of the modules
        # in case it is a fucntion or method we have to get its path using the list of imports we have from the
        # visit_ImportFrom method
        for i in range(len(modules)):
            for j in range(len(struct.import_list)):
                # if we are importing a function or class, then the part after the import in (from .. import ..)
                # will be same as the name in the __all__ list
                if len(struct.import_list[j].rsplit(".", 1)) == 2 and modules[i] == \
                        struct.import_list[j].rsplit(".", 1)[1]:
                    modules[i] = struct.import_list[j]
                    break

        # add the list of modules under the keys ['package__all__list']['the_package_name']
        struct.add__all__(struct.module_path.replace(".__init__", ""), modules)
        struct.import_list = []
        struct.list__all__ = False

    def print_indented(self, s):
        indentation = " " * self.indent
        for line in str(s).splitlines():
            print(indentation + line)

    def visit_children(self, node):
        self.indent += 2
        self.generic_visit(node)
        self.indent -= 2


if __name__ == '__main__':

    # this will create a text file with parsed data for library Pytorch
    if torch_installed:
        struct = Structure()
        parse_torch()
    else:
        print("Warning: Pytorch library is not installed on your device")
        print("if you have installed this plugin to use with Pytorch, make sure you install the library first "
              "and then run the program again")

    if sklearn_installed:
        struct = Structure()
        parse_sklearn()
    else:
        print("warning: sklearn library is not installed on your device")
        print("if you have installed this plugin to use with Sci-Kit-learn, make sure you install the library first"
              " and then run the program again")

    #
    # TestDirectory as a test
    library = TestDirectory.__file__
    library = library.replace("__init__.py", '')
    path_to_delete = library.rsplit('TestDirectory', 1)[0]
    struct = Structure()
    read_directory(library, path_to_delete, struct)
    json_object = struct.toJSON()

    # to print our structure in JSON format
    # print(json_object)

    # to write our json data to a txt file
    with open('testTextFile.txt', 'w') as outfile:
        json.dump(json_object, outfile)
