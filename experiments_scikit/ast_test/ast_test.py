import ast
import json
from implementation import Structure
from typing import Any


# i don't think we need to save the name of the classes, at for the first use case, as some files don't have classes and
# only have methods in them see (_kmeans) file for reference
# so avoiding the inclusion of names of the classes in our structure (my_struct.dict) will make our structure
# more consistent in that we always know the first keys are always the function names


class MyNodeVisitor(ast.NodeVisitor):
    indent = 0

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        # my_struct.cls_name represents the name of our class
        my_struct.cls_name = node.name
        my_struct.add_class(my_struct.cls_name)

        self.visit_children(node)

        # assign the name of the class to null after parsing the functions that are in the class
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


if __name__ == '__main__':
    # save the name of the file, so that later we can save our text file with the json data under the same name
    s = "SVC"

    f = open(s + ".py", mode="r")
    my_struct = Structure()
    contents = f.read()
    tree = ast.parse(contents)
    MyNodeVisitor().visit(tree)

    # added this to test that the object()
    # only included the test key to demonstrate that the data in the json_object is in json format
    # in json false is written with a small f unlike python

    # to turn our data in dict to be in json format, we use command dumps
    json_object = json.dumps(my_struct.dict, indent=3)

    print()
    print("this is the python reprsentation of our data")
    print(my_struct.dict)
    print()
    print("this is the json reprsentation of our data")
    print(json_object)

    # to write our json data to a txt file
    with open(s + '.txt', 'w') as outfile:
        json.dump(json_object, outfile)
