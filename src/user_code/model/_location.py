from __future__ import annotations  # https://www.python.org/dev/peps/pep-0563/

import ast
from dataclasses import dataclass
from typing import Union


@dataclass
class Location:
    file: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"'{self.file}' ({self.line}:{self.column})"

    @staticmethod
    def create_location(file: str, node: Union[ast.stmt, ast.expr]) -> Location:
        return Location(file, node.lineno, node.col_offset)
