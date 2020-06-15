import ast

from library.model import Package
from user_code.model import Imports, Location
from user_code.model._imports import Import


class ImportVisitor(ast.NodeVisitor):
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

    missing so far
    import X.*
    """

    def __init__(self, file_to_analyze: str, package: Package):
        self.file_to_analyze = file_to_analyze
        self.package = package
        self.imports = Imports()

    def visit_Import(self, node: ast.Import):
        location = Location.create_location(self.file_to_analyze, node)

        for imported in node.names:
            alias = self._get_alias(imported)
            full_name = imported.name
            self.imports.add_import(Import(alias, full_name, location))

    def visit_ImportFrom(self, node: ast.ImportFrom):
        location = Location.create_location(self.file_to_analyze, node)

        if self._is_relative_import(node):
            raise ValueError(f"{location}: Unable to handle relative imports, use absolute imports instead.")

        for imported in node.names:
            if self._is_star_import(imported):
                raise ValueError(f"{location}: Unable to handle * imports, use explicit imports instead.")
            else:
                alias = self._get_alias(imported)
                full_name = node.module + '.' + imported.name
                self.imports.add_import(Import(alias, full_name, location))

    @staticmethod
    def _get_alias(imported: ast.alias) -> str:
        return imported.name if imported.asname is None else imported.asname

    @staticmethod
    def _is_relative_import(node: ast.ImportFrom) -> bool:
        return node.level > 0

    @staticmethod
    def _is_star_import(imported_name: ast.alias) -> bool:
        return imported_name.name == '*'
