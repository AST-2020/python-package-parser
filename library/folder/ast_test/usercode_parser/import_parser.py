import ast
from typing import Any

from imports import Imports

'''
A class to save imports belonging to a given package e.g. torch or sklearn
class object iterates over parsed user code and saves recognised
imports in an Imports object

should work on following kinds of imports

import x as y, z as ...
from x import y,z,..
import x as *
'''


class ImportVisitor(ast.NodeVisitor):
    def __init__(self, module, source):
        ast.NodeVisitor.__init__(self)
        self.module = module
        self.imports = Imports()
        self.source = source

    def get_imports(self):
        return self.imports

    def visit_Import(self, node: ast.Import) -> Any:
        print(ast.dump(node))
        for alias in node.names:
            package = alias.name
            if alias.asname is None:
                asname = alias.name
            else:
                asname = alias.asname
            # load in imports
            self.imports.add_named_import(asname=asname, package=package)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        # print(ast.dump(node))
        for alias in node.names:
            if self.module in node.module.split('.'):
                if alias.asname is None:
                    if alias.name == '*':
                        package = node.module
                        self.imports.add_unnamed_import(package=package)
                        cont = self.source['package__all__list'][package]
                        self.imports.set_package_content(package=package, contents=cont)
                    else:
                        asname = alias.name
                        package = node.module + '.' + alias.name
                        self.imports.add_named_import(asname=asname, package=package)
                else:
                    asname = alias.asname
                    package = node.module + '.' + alias.name
                    self.imports.add_named_import(asname=asname, package=package)
