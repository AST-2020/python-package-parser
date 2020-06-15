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
    imports = import_visitor.imports

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

    def __init__(self, file: str, package: Package, imports, variables: Variables = Variables()):
        self.file: str = file
        self.package: Package = package
        self.imports: Imports = imports
        self.vars: Variables = variables
        self.calls = []

    def visit_Call(self, node: ast.Call) -> Any:
        self.calls.append(
            FunctionCall(
                self._get_function_name(node),
                self._get_number_of_positional_args(node),
                self._get_keyword_arg_names(node),
                self._get_callee_candidates(node),
                Location.create_location(self.file, node)
            )
        )

    @staticmethod
    def _get_function_name(node: ast.Call) -> str:
        """
        Returns the name of the function.

        Example:
            For a.b.c() this returns 'c'.
        """

        return FunctionVisitor._get_full_function_name(node).split(".")[-1]

    @staticmethod
    def _get_function_receiver(node: ast.Call) -> Optional[str]:
        """
        Returns the receiver of the function call or None if it has none.

        Example:
            For a.b.c() this returns 'a.b'.
        """

        function_path = FunctionVisitor._get_full_function_name(node).split(".")
        if len(function_path) > 1:
            return ".".join(function_path[:-1])
        else:
            return None

    @staticmethod
    def _get_full_function_name(node: ast.Call) -> str:
        """
        Returns the individual components of the full path to the function.

        Example:
            For a.b.c() this returns 'a.b.c'.
        """

        return FunctionVisitor._do_get_full_function_name(node.func)

    @staticmethod
    def _do_get_full_function_name(node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{FunctionVisitor._do_get_full_function_name(node.value)}.{node.attr}"
        else:
            raise TypeError(f"Cannot handle node type {type(node)}.")

    @staticmethod
    def _get_number_of_positional_args(node: ast.Call) -> int:
        return len(node.args)

    @staticmethod
    def _get_keyword_arg_names(node: ast.Call) -> List[str]:
        return [keyword.arg for keyword in node.keywords]

    def _get_callee_candidates(self, node: ast.Call) -> List[Function]:
        klass_name, module_name = self._get_package(node)

        if (module_name is not None) and (module_name != ""):
            return self.get_matching_overloads(self.package, module_name, klass_name, self._get_function_name(node))

        return []

    def _get_package(self, node: ast.Call):
        line = node.lineno
        name = self._get_function_name(node)
        prefix = self._get_function_receiver(node)

        if self._is_top_level_function_call(prefix, line):
            pass

        if prefix is None:
            if self.imports.resolve_alias(name, line) is not None:
                return None, self._get_function_package('', name, line)
        else:
            if self.imports.resolve_alias(prefix, line) is not None:
                return None, self._get_function_package(prefix, name, line)
            cls = self.vars.get_var_type(prefix, line)
            if cls is not None:
                return cls, self._get_method_package(cls, line)
        return None, ''

    def _is_top_level_function_call(self, prefix: Optional[str], line: int) -> bool:
        return prefix is None or self.imports.resolve_alias(prefix, line) is not None

    def _get_function_package(self, prefix: str, name: str, line: int) -> str:
        if prefix == '':
            package = self.imports.resolve_alias(name, line).split(".")
            if name == package[-1]:
                package = package[:-1]
            package = ".".join(package)
            return package
        else:
            return self.imports.resolve_alias(prefix, line)

    def _get_method_package(self, cls: str, line: int) -> str:
        if cls != '':
            cls = cls.split(".")
            package = self.imports.resolve_alias(cls[0], line).split(".")
            cls = ".".join(cls)
            if cls == package[-1]:
                package = package[:-1]
            package = ".".join(package)
            return package
        return ''

    @staticmethod
    def get_matching_overloads(package: Package, module_path: str, class_name: Optional[str],
                               func_name: str) -> List[Function]:
        if FunctionVisitor._is_constructor_call(package, module_path, class_name, func_name):
            class_name = func_name
            return package.get_methods_with_name(module_path, class_name, "__init__")
        elif FunctionVisitor._is_method_call(package, module_path, class_name, func_name):
            return package.get_methods_with_name(module_path, class_name, func_name)
        else:
            return package.get_top_level_functions_with_name(module_path, func_name)

    @staticmethod
    def _is_constructor_call(package: Package, module_path: str, class_name: Optional[str], func_name: str) -> bool:
        return len(package.get_classes_with_name(module_path, func_name)) > 0 or \
               class_name is not None and func_name == class_name

    @staticmethod
    def _is_method_call(package: Package, module_path: str, class_name: Optional[str], func_name: str) -> bool:
        return not FunctionVisitor._is_constructor_call(package, module_path, class_name, func_name) and \
               class_name is not None
