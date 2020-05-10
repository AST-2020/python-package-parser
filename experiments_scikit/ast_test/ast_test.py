import ast
import json
import os
from implementation import Structure
from typing import Any


# um den Logik hinter das Struktur zu zeige, haben wir ein Directory erstellt, heißt "TestDirectory"
# und das Parsing Ergebnis ist in testTesxtFile.txt
# und zu zeigen, wie man info von dem Struktur erhalten, ahben wir zwei Datein, heißen: "tester.py" "file_to_test.py"


def read_directory(directory):
    for entry in os.scandir(directory):
        path = directory + "/" + entry.name
        my_struct.module_path = path.replace("/", ".")
        if path.endswith(".py"):
            my_struct.module_path = my_struct.module_path.replace(".py", "")
            # had to ensure encoding is UTF-8 to avoid an error
            f = open(path, mode="r", encoding='utf-8')
            contents = f.read()
            tree = ast.parse(contents)
            MyNodeVisitor().visit(tree)

            my_struct.module_path = None
        # if file is not a py file, then test if it's a directory, if so
        # then call the read_directory recursively on that directory passing its complete path
        elif not entry.name.startswith('.') and entry.is_dir():
            read_directory(path)


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        # my_struct.cls_name represents the name of our class
        my_struct.cls_name = node.name
        my_struct.add_class_path(my_struct.module_path)
        my_struct.add_class_name(my_struct.module_path, my_struct.cls_name)
        self.visit_children(node)
        # assign the name of the class to null after parsing the functions that are in that class
        my_struct.cls_name = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        args = [arg.arg for arg in node.args.args]
        if my_struct.cls_name is None:
            if my_struct.module_path not in list(my_struct.dict["function"].keys()):
                my_struct.add_module(my_struct.module_path)
            my_struct.add_func(my_struct.module_path, node.name, args)
        else:
            my_struct.add_method(my_struct.module_path, my_struct.cls_name, node.name, args)

    # to parse the import statements in the __init__.py in the package, if it exists
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if "__init__" not in my_struct.module_path:
            return
        imports = [["" if node.module is None or node.module is "." else node.module,
              obj.name] for obj in node.names]
        for imported in imports:
            my_struct.import_list.append(imported)

    # to test if the name of the variable is __all__ (variable is list in this case)
    def visit_Name(self, node: ast.Name):
        if node.id is "__all__":
            my_struct.list__all__ = True

    # to parse the __all__ list in the __init__.py that is included in every packages, if it exists
    def visit_List(self, node: ast.List):
        if "__init__" not in my_struct.module_path or not my_struct.list__all__:
            return
        # to get all the names of the modules in the __all__ list
        modules = [obj.s for obj in node.elts]
        # to get the relative paths of the modules
        for i in range(len(modules)):
            for j in range(len(my_struct.import_list)):
                if modules[i] in my_struct.import_list[j][1]:
                    modules[i] = [my_struct.import_list[j][0], my_struct.import_list[j][1]]
                    break
            else:
                modules[i] = ["", modules[i]]
        # add the list of modules under the keys ['package__all__list']['the_package_name']
        my_struct.add__all__(my_struct.module_path.replace(".__init__", ""), modules)
        my_struct.import_list = []
        my_struct.list__all__ = False

    def print_indented(self, s):
        indentation = " " * self.indent
        for line in str(s).splitlines():
            print(indentation + line)

    def visit_children(self, node):
        self.indent += 2
        self.generic_visit(node)
        self.indent -= 2


if __name__ == '__main__':
    # save the name of the folder, where the library is
    library = 'sklearn'
    my_struct = Structure()
    read_directory(library)

    json_object = my_struct.toJSON()
    # to print our structure in JSON format
    print(json_object)

    # to print our results in python format
    # print(my_struct.dict)

    # to write our json data to a txt file
    with open('resultsSciKit.txt', 'w') as outfile:
        json.dump(json_object, outfile)
