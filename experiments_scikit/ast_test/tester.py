import ast
import json
import os
from typing import Any
from implementation import Structure


class Simple_Structure():
    def __init__(self):
        self.to_test_packages = []


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    # to parse the import statements
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        imports = [["" if node.module is None or node.module is "." else node.module,
                    obj.name] for obj in node.names]
        for imported in imports:
            my_struct.to_test_packages.append(imported)
        # print(my_struct.to_test_packages)

    def visit_Import(self, node: ast.Import) -> Any:
        my_struct.to_test_packages.append([obj.name for obj in node.names])
        # print(my_struct.to_test_packages)

    # to test if the name of the variable is __all__ (variable is list in this case)
    def visit_Name(self, node: ast.Name):
        if node.id is "__all__":
            my_struct.list__all__ = True

    def print_indented(self, s):
        indentation = " " * self.indent
        for line in str(s).splitlines():
            print(indentation + line)

    def visit_children(self, node):
        self.indent += 2
        self.generic_visit(node)
        self.indent -= 2


if __name__ == '__main__':
    my_struct = Simple_Structure()
    file = 'file_to_test.py'
    f = open(file, mode="r", encoding='utf-8')
    contents = f.read()
    tree = ast.parse(contents)
    MyNodeVisitor().visit(tree)

    # file to read our saved data from the json file
    with open('testTesxtFile.txt') as json_file:
        json_obj = json.load(json_file)
    data = json.loads(json_obj)
    # print(data)

    print(my_struct.to_test_packages, "\n")
    # every entry represents an import statement
    # and they are saved as (from, import)
    # where the first part is the string after the from and the second part is the string after the import
    for package in my_struct.to_test_packages:
        # if we imported a whole (.py) module
        # it means that i will find the path under both keys "function" and "method"
        if package[0] + "." + package[1] in data['method'] and package[0] + "." + package[1] in data['function']:
            print("import the whole file")
            print("parameters in Method ", data['method'][package[0] + "." + package[1]])
            print("parameters in Function ", data['function'][package[0] + "." + package[1]], "\n")

        # if we imported a class
        # then i will find the first part of the import (from) under the method key
        # and the second part under ["method"]["from..."]
        elif package[0] in data['method'] and package[1] in data['method'][package[0]]:
            print("only imported the class")
            print("parameters in Method ", data['method'][package[0]][package[1]], "\n")

        # if we imported a function
        # then i will find the first part of the import (from) under the function key
        # and the second part under ["function"]["from..."]
        elif package[0] in data['function'] and package[1] in data['function'][package[0]]:
            print("only imported the function")
            print("parameters in Function ", data['function'][package[0]][package[1]], "\n")

        # if we imported a package
        # if we have reached this statement
        # then it means we have imported a package and we should look at what is specified in the __all__ list in
        # the __init__ file
        else:
            all_string = package[0] + "." + package[1]
            all_string = all_string.replace(".*", "")
            # to get the imported modules, classes and fucntions that are specified in the __all__ list
            functions_and_classes = data['package__all__list'][all_string]
            print("imported using __all__")
            # we add the module, class or function path to the path of the package
            for realtive_path in functions_and_classes:
                ### same as before we see if what eas imported, is a .py file
                if all_string + "." + realtive_path[0] in data["method"] and realtive_path[1] \
                        in data["method"][all_string + "." + realtive_path[0]]:
                    print("parameters in Method ", data["method"][all_string + "." + realtive_path[0]])

                if all_string + "." + realtive_path[0] in data["function"] and realtive_path[1] \
                        in data["function"][all_string + "." + realtive_path[0]]:
                    print("parameters in function ", data["function"][all_string + "." + realtive_path[0]])
                ###

                # or a single class
                if all_string + "." + realtive_path[0] + realtive_path[1] in data["method"]:
                    print("parameters in Method ",
                          data["method"][all_string + "." + realtive_path[0] + realtive_path[1]])

                # or a function
                if all_string + "." + realtive_path[0] + realtive_path[1] in data["function"]:
                    print("parameters in function ",
                          data["function"][all_string + "." + realtive_path[0] + realtive_path[1]])

                # and as a last test we see if it is a function or class in the __init__ file itself
                # will write it in next iteration
