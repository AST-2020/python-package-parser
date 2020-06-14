import ast
from typing import Any, Optional, List

from analysis.check_arg_names import check_arg_names
from analysis.check_arg_number import check_arg_number
from analysis.message import MessageManager
from library.model import Package, Function
from user_code.model import FunctionCall, Imports, Variables, Location
from user_code.parser._import_parser import ImportVisitor
from user_code.parser._variable_parser import VariableVisitor


def parse_function_calls(file_to_analyze: str, package: Package) -> List[FunctionCall]:
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

    fp = FunctionVisitor(file_to_analyze, package, imps, vars)
    fp.visit(tree)

    return fp.calls


class FunctionVisitor(ast.NodeVisitor):
    """
    this visitor scans for function and method calls. functions and methods, which can be assigned to the module
    will be further analysed to gather information about its position in the module, name, line, arguments.
    This information is then used to call a analyses method to evaluate its correctness.
    """

    def __init__(self, file, package: Package, imports, variables: Variables = Variables()):
        ast.NodeVisitor.__init__(self)
        self.imports: Imports = imports
        self.vars: Variables = variables
        self.package = package
        self.file = file
        self.calls = []
        self.message_manager = MessageManager()

    def visit_Call(self, node: ast.Call) -> Any:
        # note that name contains class obj name as well if method
        receiver, name = self._get_name(node)
        cls, package = self._get_package(receiver, name, node.lineno)

        call = self._create_function_call(node)

        self.calls.append(call)

        if cls == '':
            cls = None

        if (package is not None) and (package != ""):
            # compare names of named args
            check_arg_names(self.message_manager, call, self.package, package, name, cls)
            # compare arg count
            check_arg_number(self.message_manager, call, self.package, package, name, cls)

    def _create_function_call(self, node: ast.Call) -> FunctionCall:
        return FunctionCall(
            self._get_callee(node),
            self._get_number_of_positional_args(node),
            self._get_keyword_arg_names(node),
            Location.create_location(self.file, node)
        )

    def _get_callee(self, node: ast.Call) -> List[Function]:
        pass

    @staticmethod
    def _get_number_of_positional_args(node: ast.Call) -> int:
        return len(node.args)

    @staticmethod
    def _get_keyword_arg_names(node: ast.Call) -> List[str]:
        return [keyword.arg for keyword in node.keywords]

    def _get_package(self, prefix, name, line):
        if prefix is None:
            if self.imports.get_package_from_asname(name, line) is not None:
                return '', self._get_function_package('', name, line)

        else:
            if self.imports.get_package_from_asname(prefix, line) is not None:
                return '', self._get_function_package(prefix, name, line)
            cls = self.vars.get_var_type(prefix, line)
            if cls is not None:
                return cls, self._get_method_package(cls, name, line)
        return '', ''

    def _get_function_package(self, prefix, name, line):
        if prefix == '':
            package = self.imports.get_package_from_asname(name, line).split('.')
            if name == package[-1]:
                package = package[:-1]
            package = '.'.join(package)
            return package
        else:
            return self.imports.get_package_from_asname(prefix, line)

    def _get_method_package(self, cls, name, line):
        if cls != '':
            cls = cls.split('.')
            package = self.imports.get_package_from_asname(cls[0], line).split('.')
            cls = '.'.join(cls)
            if cls == package[-1]:
                package = package[:-1]
            package = '.'.join(package)
            return package
        return ''

    def _get_name(self, node: ast.Call) -> (Optional[str], str):
        function_path = self._function_path(node.func)

        if len(function_path) > 1:
            return '.'.join(function_path[:-1]), function_path[-1]
        else:
            return None, function_path[0]

    def _function_path(self, node: ast.AST) -> List[str]:
        if isinstance(node, ast.Name):
            return [node.id]
        elif isinstance(node, ast.Attribute):
            result = self._function_path(node.value)
            result.append(node.attr)
            return result
        else:
            raise ValueError(f"Cannot handle node type {type(node)}.")
