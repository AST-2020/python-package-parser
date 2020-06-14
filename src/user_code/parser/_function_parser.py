import ast
from typing import Any, Optional, List

from library.model import Package, Function
from user_code.model import FunctionCall, Imports, Variables, Location
from user_code.parser._import_parser import ImportVisitor
from user_code.parser._variable_parser import VariableVisitor


def parse_function_calls(file_to_analyze: str, package: Package) -> List[FunctionCall]:
    with open(file_to_analyze, mode='r') as f:
        contents = f.read()
        tree = ast.parse(contents)

    # get imports
    import_visitor = ImportVisitor(file_to_analyze, package)
    import_visitor.visit(tree)
    imports = import_visitor.get_imports()

    # get vars
    var_visitor = VariableVisitor(imports)
    var_visitor.visit(tree)
    variables = var_visitor.get_vars()

    fp = FunctionVisitor(file_to_analyze, package, imports, variables)
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
        self.package: Package = package
        self.file = file
        self.calls = []

    def visit_Call(self, node: ast.Call) -> Any:
        _, func_name = self._get_name(node)
        call = FunctionCall(func_name, self._get_number_of_positional_args(node), self._get_keyword_arg_names(node),
                            self._get_callee(node), Location.create_location(self.file, node))
        self.calls.append(call)

    def _get_callee(self, node: ast.Call) -> List[Function]:
        receiver, func_name = self._get_name(node)
        cls, package = self._get_package(receiver, func_name, node.lineno)

        if (package is not None) and (package != ""):
            return get_matching_overloads(self.package, package, func_name, cls)

        return []

    @staticmethod
    def _get_number_of_positional_args(node: ast.Call) -> int:
        return len(node.args)

    @staticmethod
    def _get_keyword_arg_names(node: ast.Call) -> List[str]:
        return [keyword.arg for keyword in node.keywords]

    def _get_package(self, prefix, name: str, line: int):
        if prefix is None:
            if self.imports.get_package_from_asname(name, line) is not None:
                return None, self._get_function_package('', name, line)

        else:
            if self.imports.get_package_from_asname(prefix, line) is not None:
                return None, self._get_function_package(prefix, name, line)
            cls = self.vars.get_var_type(prefix, line)
            if cls is not None:
                return cls, self._get_method_package(cls, line)
        return None, ''

    def _get_function_package(self, prefix: str, name: str, line: int) -> str:
        if prefix == '':
            package = self.imports.get_package_from_asname(name, line).split('.')
            if name == package[-1]:
                package = package[:-1]
            package = '.'.join(package)
            return package
        else:
            return self.imports.get_package_from_asname(prefix, line)

    def _get_method_package(self, cls: str, line: int) -> str:
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
            raise TypeError(f"Cannot handle node type {type(node)}.")


def get_matching_overloads(package: Package, module_path: str, func_name: str,
                           cls_name: Optional[str]) -> List[Function]:
    if _is_constructor_call(package, module_path, func_name, cls_name):
        return package.get_methods_with_name(module_path, func_name, "__init__")
    elif _is_method_call(package, module_path, func_name, cls_name):
        return package.get_methods_with_name(module_path, cls_name, func_name)
    else:
        return package.get_top_level_functions_with_name(module_path, func_name)


def _is_constructor_call(package: Package, module_path: str, func_name: str, cls_name: str) -> bool:
    return len(package.get_classes_with_name(module_path, func_name)) > 0 or \
           cls_name is not None and func_name == cls_name


def _is_method_call(package: Package, module_path: str, func_name: str, cls_name: Optional[str]) -> bool:
    return not _is_constructor_call(package, module_path, func_name, cls_name) and cls_name is not None
