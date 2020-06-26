import ast
from typing import Any, Optional, List

from library.model import Package, Function
from user_code.model import FunctionCall, Imports, Variables, Location
from user_code.parser._import_parser import ImportVisitor
from user_code.parser._variable_parser import VariableVisitor
from user_code.model.argument import Arg, Kw_arg
from user_code.parser._all_variable_parser import AllVariableVisitor
from user_code.model import Variable

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

    # get all declared vars
    declared_vars = FunctionVisitor(file_to_analyze,package, imports, variables)
    declared_vars.get_declared_vars()


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
                self._get_positional_arg(node, self.get_declared_vars()), #--
                self._get_keyword_arg(node, self.get_declared_vars()), #--
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

    @staticmethod #--
    def _get_keyword_arg(node: ast.Call,  declared_vars) -> List[Kw_arg]:
        """
        Returns all keywords arguments as List of kw_arg object.

        """
        kws = []
        for keyword in node.keywords:
            arg_type = None
            if isinstance(keyword.value, ast.Name):
                value_var_name = keyword.value.id
                arg_value, var_type = FunctionVisitor.find_value(declared_vars, value_var_name, keyword.value.lineno)
                # print(str(arg_value))
                if var_type is not None:
                    arg_type = var_type
            elif isinstance(keyword.value, ast.Dict):
                arg_type = type({})
                arg_value = getattr(keyword.value,keyword.value.__dir__()[0])
            else:
                arg_value = getattr(keyword.value,keyword.value.__dir__()[0])
            a = Kw_arg(keyword.arg, arg_value)
            if arg_type != None:
                a.set_typ(arg_type)
            kws.append(a)
        return kws

    @staticmethod
    def find_value(var: AllVariableVisitor, var_name, var_lineno) -> Any:
        vars:[Variable] = []
        value = None
        var_type = None
        last_line_nr = 0
        var = var
        for variable in var:
            if var_name == variable.name:
                # print(vars[name][0], vars[name][1])
                if var_lineno > variable.lineno and variable.lineno > last_line_nr:
                    value = variable.value
                    var_type = variable.get_type()
                    last_line_nr = variable.lineno
        return value, var_type

    def get_declared_vars(self):
        with open(self.file, mode='r') as f:
            contents = f.read()
        tree = ast.parse(contents)
        declared_vars = AllVariableVisitor()
        declared_vars.visit(tree)
        return declared_vars.usedvars


    @staticmethod #---
    def _get_positional_arg(node: ast.Call, declared_vars) -> List[Arg]:
        """
        Returns all positional arguments as List of Arg object.

        """
        args = []

        for arg in node.args:
            if isinstance(arg, ast.Name):
                arg_value, arg_type = FunctionVisitor.find_value(declared_vars, arg.id, arg.lineno )
                a = Arg(arg_value)
                if arg_type is not None:
                    a.set_typ(arg_type)
                args.append(a)
            else:
                if isinstance(arg, ast.Dict):
                    a = Arg(getattr(arg, arg.__dir__()[0]))
                    a.set_typ(type({}))
                else:
                    a = Arg(getattr(arg, arg.__dir__()[0]))
                args.append(a)
        return args





    def _get_callee_candidates(self, node: ast.Call) -> List[Function]:
        module_path, class_name, function_name = self.find_function(node)

        if module_path is None:
            return []
        elif FunctionVisitor._is_constructor_call(self.package, module_path, function_name):
            class_name = function_name
            return self.package.get_methods_with_name(module_path, class_name, "__init__")
        elif FunctionVisitor._is_method_call(self.package, module_path, class_name, function_name):
            return self.package.get_methods_with_name(module_path, class_name, function_name)
        else:
            return self.package.get_top_level_functions_with_name(module_path, function_name)

    def find_function(self, node: ast.Call) -> (Optional[str], Optional[str], str):
        function_name = self._get_function_name(node)
        line = node.lineno

        receiver = self._get_function_receiver(node)
        if receiver is None:  # Direct call: f()
            if self.imports.resolve_alias(function_name, line) is not None:
                module_path = self.imports.get_module_path(function_name, line)
                return module_path, None, function_name
        else:
            if self.imports.resolve_alias(receiver, line) is not None:  # Qualified call: module.f()
                module_path = self.imports.resolve_alias(receiver, line)
                return module_path, None, function_name
            else:
                class_name = self.vars.get_var_type(receiver, line)
                if class_name is not None:  # Method call: var.f()
                    module_path = self.imports.get_module_path(class_name, line)
                    return module_path, class_name, function_name

        return None, None, function_name

    @staticmethod
    def _is_constructor_call(package: Package, module_path: str, func_name: str) -> bool:
        return len(package.get_classes_with_name(module_path, func_name)) > 0

    @staticmethod
    def _is_method_call(package: Package, module_path: str, class_name: Optional[str], func_name: str) -> bool:
        return not FunctionVisitor._is_constructor_call(package, module_path, func_name) and class_name is not None

    def _is_top_level_function_call(self, prefix: Optional[str], line: int) -> bool:
        return prefix is None or self.imports.resolve_alias(prefix, line) is not None


if __name__ == '__main__':
    with open('..\..\example.py', mode='r') as f:
        contents = f.read()
        tree = ast.parse(contents)


    vars = AllVariableVisitor()
    vars.visit(tree)
    declared_vars = vars.usedvars
    # print(declared_vars)
    # # print(usedvars.usedvars)
    # print(FunctionVisitor.find_value(var=declared_vars, var_name='N', var_lineno = 20))


    # l = []
    # l.extend(FunctionVisitor.get_declared_vars(tree))
    # for k in l:
    #     k.print_variable()


    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # l = []
            kwl: [Kw_arg] = []
            #l.extend(FunctionVisitor._get_positional_arg(node, declared_vars ))
            kwl.extend(FunctionVisitor._get_keyword_arg(node, declared_vars))
            print('method')
            #for k in l:
            #    k.print_arg()
            for k0 in kwl:
                k0.print_kw_arg()
