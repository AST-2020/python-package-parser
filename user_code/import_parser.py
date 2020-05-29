"""
A class to save imports belonging to a given package e.g. torch or sklearn in imports,
class object iterates over parsed user code and saves recognised imports,
also ignores not relevant imports.

should work on following kinds of imports:
import X
import X as Y
import X as A, Y as B, ...

from X import Y
from X import Y, Z, ...
from X import Y as A
from X import *

missing so far
import X.*
"""

import ast
from typing import Any

from user_code.imports import Imports


class ImportVisitor(ast.NodeVisitor):
    # module is the module name to check for
    # source is the structure in which the modules infos about submodules,.. are stores
    def __init__(self, module, source):
        ast.NodeVisitor.__init__(self)
        self.module = module
        self.imports = Imports()
        self.source = source

    def get_imports(self):
        return self.imports

    def del_imports(self):
        self.imports = Imports()

    # watches all import ... statements and extracts info
    def visit_Import(self, node: ast.Import) -> Any:
        line = node.lineno
        for alias in node.names:
            package = alias.name
            # check if asname is used or not
            if alias.asname is None:
                # if asname is not used take latest name part as asname
                asname = alias.name.split('.')[-1]
            else:
                asname = alias.asname
            # load in imports
            if self.module in package:
                self.imports.add_named_import(asname=asname, package=package, line=line)

    # watches all from ... import ... statements and extracts info
    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        line = node.lineno
        for alias in node.names:
            if self.module in node.module.split('.'):
                # if there is no asname
                if alias.asname is None:
                    # if a star import is used store info in imports.unknown
                    if alias.name == '*':
                        package = node.module
                        self.imports.add_unnamed_import(package=package, line=line)
                        cont = self.source['package__all__list'][package]
                        self.imports.set_package_content(package=package, contents=cont)

                    # else generate the asname from name and store in imports.named
                    else:
                        asname = alias.name
                        package = node.module + '.' + alias.name
                        self.imports.add_named_import(asname=asname, package=package, line=line)

                # if asname is given in import store in imports.named
                else:
                    asname = alias.asname
                    package = node.module + '.' + alias.name
                    self.imports.add_named_import(asname=asname, package=package, line=line)
