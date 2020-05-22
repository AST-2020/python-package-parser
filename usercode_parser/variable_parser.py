"""
A class to save variable declarations in an UsedVariable object
it gets name, prefix and the line it is defined in
and saves it in the object if it is included with the imports stored in imports
Therefore variables which belong to the library, but are not imported correctly are ignored and not added!
"""

import ast
from typing import Any

from variables import UsedVariables
from imports import Imports


class VariableVisitor(ast.NodeVisitor):
    def __init__(self, imports: Imports = Imports()):
        ast.NodeVisitor.__init__(self)
        self.vars: UsedVariables = UsedVariables()
        self.imports: Imports = imports

    # becuase we assume that all varables need to have type annotations
    # we only need to pay attention to ast.AnnAssign nodes
    def visit_AnnAssign(self, node: ast.AnnAssign) -> Any:
        # var name and line
        name = node.target.id
        line = node.lineno

        # if the type annotation has a prefix
        if isinstance(node.annotation, ast.Attribute):
            # get type and the import path
            type = node.annotation.value.id

            for key in self.imports.named:
                if type == key:
                    type += '.' + node.annotation.attr
                    self.vars.add_usage(var=name, type=type, line=line)

        else:
            # if the constructor is the prefix
            type = node.annotation.id
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

    def get_vars(self):
        return self.vars
