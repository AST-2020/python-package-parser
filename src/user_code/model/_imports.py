from __future__ import annotations  # https://www.python.org/dev/peps/pep-0563/

from dataclasses import dataclass
from typing import Dict, Optional

from user_code.model._location import Location


class Imports:
    """
    Imports class stores all used imports. in named imports later called by a name prefix are stored,
    and in unknown imports without a prefix needed are stored
    """

    def __init__(self):
        self.imports: Dict[str, Import] = {}

    def add_import(self, imp: Import):
        self.imports[imp.alias] = imp

    def resolve_alias(self, alias: str, line: int) -> Optional[str]:
        if self._is_imported_already(alias, line):
            return self.imports[alias].full_name
        else:
            return None

    def get_module_path(self, alias: str, line: int) -> Optional[str]:
        full_name = self.resolve_alias(alias, line)
        if full_name is None:
            return None

        # Remove the part of the full name after the last dot if it is the same as the alias
        full_name_parts = full_name.split(".")
        if alias == full_name_parts[-1]:
            full_name_parts = full_name_parts[:-1]
        return ".".join(full_name_parts)

    def _is_imported_already(self, alias: str, line: int) -> bool:
        return alias in self.imports and line >= self.imports[alias].location.line


@dataclass
class Import:
    alias: str
    full_name: str
    location: Location
