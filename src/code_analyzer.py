import ast
import sys

from library.model import Package
from library.parser import parse_package
from user_code.parser import FunctionVisitor, ImportVisitor, VariableVisitor


def parse_code(file_to_analyze: str, package: Package):
    """
    This function combines all of the python files to first visit the user code 'file' for imports, then variables, then
    functions and methods.
    """

    # open file
    with open(file_to_analyze, mode='r') as f:
        contents = f.read()
        tree = ast.parse(contents)

    # get imports
    imp = ImportVisitor(package.get_name(), package)
    imp.visit(tree)
    imps = imp.get_imports()

    # get vars
    var = VariableVisitor(imps)
    var.visit(tree)
    vars = var.get_vars()

    # inspect functions
    fp = FunctionVisitor(file_path, package, imps, vars)
    fp.visit(tree)

    fp.message_manager.print_messages()

    # TODO get all functions calls, loop over them and check each one
    # TODO actually to find the callee we must already do the checks in the analysis (in case there are overloads or an
    #  import is missing)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]

        # parse torch and sklearn library
        torch = parse_package('torch')
        sklearn = parse_package('sklearn')

        # parse code for both libraries
        parse_code(file_path, torch)
        parse_code(file_path, sklearn)

    else:
        print('Usage: python code_analyzer.py <file_to_analyze>')
