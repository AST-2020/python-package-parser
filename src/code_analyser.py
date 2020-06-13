import ast
import sys

from library.library_model import Library
from library.package_parser import parse_package
from user_code.code_parser import FunctionVisitor
from user_code.import_parser import ImportVisitor
from user_code.variable_parser import VariableVisitor


def parse_code(file_to_analyze: str, package_name: str, package: Library):
    """
    This function combines all of the python files to first visit the user code 'file' for imports, then variables, then
    functions and methods.
    """

    # open file
    f = open(file_to_analyze, mode='r')
    contents = f.read()
    tree = ast.parse(contents)

    # get imports
    imp = ImportVisitor(package_name, package)
    imp.visit(tree)
    imps = imp.get_imports()

    # get vars
    var = VariableVisitor(imps)
    var.visit(tree)
    vars = var.get_vars()

    # inspect functions
    fp = FunctionVisitor(file_path, package, imps, vars)
    fp.visit(tree)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]

        # parse torch and sklearn library
        torch = parse_package('torch')
        sklearn = parse_package('sklearn')

        # parse code for both libraries
        parse_code(file_path, "torch", torch)
        parse_code(file_path, "sklearn", sklearn)

    else:
        print('programm expects only the file to check as an argument.')
