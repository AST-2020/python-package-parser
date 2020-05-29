import ast
import json
from typing import Any


# limitation of the program:
# 1- the program doesn't expect named imports
#   ex:
#   (import ... as x) (allowed)
#   or (from ... import ... as y) (don't know if this is allowed)
#
# 2- imports may not be handled in order, which should be okay actually for nearly all programs

class Simple_Structure:
    def __init__(self):
        self.to_test_packages = []


# where the imports from the user's code are saved
parsed_data = Simple_Structure()


def get_module(output_file, data, path):
    output_file = get_class(output_file, data, path)
    output_file = get_func(output_file, data, path)
    return output_file


def get_func(output_file, data, path, func_name=None, in_file=False):
    if func_name is None:
        for func in data["function"][path]:
            output_file["file"][path + "." + func] = data["function"][path][func]
            # print(output_file)
    else:
        output_file["function"][path + "." + func_name] = data["function"][path][func_name]
        # print(output_file)
    return output_file


def get_class(output_file, data, path, cls_name=None, in_file=False):
    if cls_name is None:
        for cls in data["method"][path]:
            output_file["file"][path + "." + cls] = data["method"][path][cls]
    else:
        output_file["method"][path + "." + cls_name] = data["method"][path][cls_name]
    return output_file


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    # to parse the from.. import.. statements
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        for obj in node.names:
            # print(node.module + "." + obj.name)
            parsed_data.to_test_packages.append(node.module + "." + obj.name)

    # to parse the import statements
    def visit_Import(self, node: ast.Import) -> Any:
        for obj in node.names:
            # print(obj.name)
            parsed_data.to_test_packages.append(obj.name)

    def print_indented(self, s):
        indentation = " " * self.indent
        for line in str(s).splitlines():
            print(indentation + line)

    def visit_children(self, node):
        self.indent += 2
        self.generic_visit(node)
        self.indent -= 2


def parse_imports(file_path):
    results = {"method": {}, "function": {}, "file": {}}
    f = open(file_path, mode="r", encoding='utf-8')
    contents = f.read()
    tree = ast.parse(contents)
    MyNodeVisitor().visit(tree)
    with open('testTextFile.txt') as json_file:
        json_obj = json.load(json_file)
        # print(json_obj)
    data = json.loads(json_obj)
    # print(data)
    for complete_path in parsed_data.to_test_packages:
        # print(struct.to_test_packages)
        # to obtain the path up to the module level in case a function or class are imported(used in 2nd and 3rd (elif))
        path_till_module_level = complete_path.rsplit('.', 1)[0]
        # to obtain the class name or the function name in case a function or class are imported
        # (used in 2nd and 3rd (elif))
        cls_or_func_name = complete_path.rsplit('.', 1)[1]

        # if we imported a whole (.py) module
        # it means that i will find the path under both keys "function" and "method"
        if complete_path in data['method'] and complete_path in data['function']:
            results = get_module(results, data, complete_path)

        # if we imported a class
        # then (find path_till_module_level) will be found under the method key
        # and (cls_or_func_name) under ["method"]["path_till_module_level"]
        elif path_till_module_level in data['method'] and cls_or_func_name in data['method'][path_till_module_level]:
            results = get_class(results, data, path_till_module_level, cls_or_func_name)

        # if we imported a function
        # then (find path_till_module_level) will be found under the funtion key
        # and (cls_or_func_name) under ["function"]["path_till_module_level"]
        elif path_till_module_level in data['function'] and cls_or_func_name in \
                data['function'][path_till_module_level]:
            results = get_func(results, data, path_till_module_level, cls_or_func_name)

        # this statement will be reached only if a package is imported
        # and the imports in the __all__ list from the __init__ file has to be considered
        else:
            # all_string represent the name of the package, which we will need to access the imported modules, class
            # and functions which will be saved under the ["package__all__list"][all_string]
            complete_path = complete_path.replace(".*", "")
            # to get the imported modules, classes and fucntions that are specified in the __all__ list
            functions_and_classes = data['package__all__list'][complete_path]
            # print(functions_and_classes)
            # we add the module, class or function path to the path of the package
            for realtive_path in functions_and_classes:
                # to test if the method imported is in the __init__ file
                if complete_path + ".__init__" in data["method"] and \
                        realtive_path in data["method"][complete_path + ".__init__"]:
                    results = get_class(results, data, complete_path + ".__init__", realtive_path)

                # to test if the function imported is in the __init__ file
                elif complete_path + ".__init__" in data["function"] and \
                        realtive_path in data["function"][complete_path + ".__init__"]:
                    results = get_func(results, data, complete_path + ".__init__", realtive_path)

                # to cover all other cases (importing a module, function or class from sub-packages)
                # idea: all the other cases can be covered by adding a new import including the
                # sub-package as a part of it to the list of imports (struct.to_test_packages)
                # (same idea as a recursive function)
                else:
                    parsed_data.to_test_packages.append(complete_path + "." + realtive_path)

    for key in results["method"].keys():
        if "__init__." in key:
            key = key.replace("__init__.", "")
    for key in results["function"].keys():
        if "__init__." in key:
            key = key.replace("__init__.", "")

    return results


if __name__ == '__main__':
    file = 'file_to_test.py'
    output = parse_imports(file)
    print(output)

    # {'method': {'TestDirectory.__init__.cls_in_init': {'__init__': ['self'], 'method_in_init': ['self', 'really_cool']},
    #             'TestDirectory.file1.testFile1': {'__init__': ['self', 'name']}},
    #  'function': {'TestDirectory.__init__.func_in_init': ['init_args', 'cool'],
    #               'TestDirectory.file1.testFunc1': ['num'],
    #               'TestDirectory.PackageInside.InsidePackageInside.__init__.extreme_case': ['really_extreme']},
    #  'file': {'TestDirectory.PackageInside.file3.testClass3': {'__init__': ['self'], 'methode3': ['self', 'args']},
    #           'TestDirectory.PackageInside.file3.testFunc3': ['num']}}
