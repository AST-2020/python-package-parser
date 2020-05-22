import ast
from typing import Any

from variables import UsedVariables
from imports import Imports


class VariableVisitor(ast.NodeVisitor):
    def __init__(self, imports: Imports = Imports()):
        ast.NodeVisitor.__init__(self)
        self.vars: UsedVariables = UsedVariables()
        self.imports: Imports = imports

    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        name = node.target.id
        line = node.lineno
        if isinstance(node.annotation, ast.Attribute):
            type = node.annotation.value.id

            for key in self.imports.named:
                if type == key:
                    type += '.' + node.annotation.attr
                    self.vars.add_usage(var=name, type=type, line=line)

        else:
            type = node.annotation.id
            # if constructor directly imported
            for key in self.imports.named:
                if type == key:
                    self.vars.add_usage(var=name, type=type, line=line)

            # if constructor imported with *
            for package in self.imports.unknown:
                for touple in self.imports.unknown[package]:
                    for item in touple:
                        # print(item)
                        if type == item:
                            self.vars.add_usage(var=name, type=type, line=line)
            # if (name in self.imports.named) or ((name in package) for package in self.imports.unknown):
            #     self.vars.add_usage(var=name, type=type, line=line)

    def get_vars(self):
        return self.vars
