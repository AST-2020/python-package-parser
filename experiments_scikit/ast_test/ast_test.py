import ast
import json
import os
from implementation import Structure
from typing import Any

# weil die Bib riesig ist, habe ich eine kleine Test Ordner heißt: test_directory, um den Logik des Programs zu sehen
# einfach statt "scikit-learn-master" "test_directory" schreiben

# das Program liest alle Datei in der Bibliothek außer diese beide Dateien:
# (könnte das lösen, dadurch dass ich den encoding von alle Dateien zu UTF-8 geändert habe)
# Zeile 57
#
# 1- scikit-learn-master/sklearn/feature_extraction/tests/test_text.py
# 2- scikit-learn-master/sklearn/preprocessing/tests/test_encoders.py


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        # my_struct.cls_name represents the name of our class
        my_struct.cls_name = node.name
        my_struct.add_class(my_struct.cls_name)

        self.visit_children(node)

        # assign the name of the class to null after parsing the functions that are in that class
        my_struct.cls_name = None

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        my_struct.add_func(node.name, my_struct.cls_name)
        if my_struct.cls_name is None:
            # it means that the function is not in a class
            my_struct.dict["global_func"][node.name] = [arg.arg for arg in node.args.args]
        else:
            my_struct.dict[my_struct.cls_name][node.name] = [arg.arg for arg in node.args.args]

    def print_indented(self, s):
        indentation = " " * self.indent
        for line in str(s).splitlines():
            print(indentation + line)

    def visit_children(self, node):
        self.indent += 2
        self.generic_visit(node)
        self.indent -= 2

    @staticmethod
    def read_directory(directory):
        for entry in os.scandir(directory):

            # to get the full path for our directory
            complete_filepath = directory + "/" + entry.name

            # if file is a py file, we parse it
            if complete_filepath.endswith(".py"):

                # had to change encoding to avoid an error asscoiated with encoding
                # you can see the error by removing the encoding parameter and running the program
                f = open(complete_filepath, mode="r", encoding='utf-8')

                contents = f.read()
                tree = ast.parse(contents)
                MyNodeVisitor().visit(tree)
                continue

            # if file is not a py file, then test if it's a directory, if so
            # then call the read_directory recursively on that directory passing its complete path
            elif not entry.name.startswith('.') and entry.is_dir():
                MyNodeVisitor.read_directory(complete_filepath)


if __name__ == '__main__':

    # save the path of the folder, where the library is
    library = 'scikit-learn-master'

    my_struct = Structure()
    MyNodeVisitor.read_directory(library)

    # to print our results in python format
    # print(my_struct.dict)

    json_object = my_struct.toJSON()
    print("\nthis is the json reprsentation of our data\n")
    print(json_object)

    # to write our json data to a txt file
    # with open('results.txt', 'w') as outfile:
    # json.dump(json_object, outfile)
