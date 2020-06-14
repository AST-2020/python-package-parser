from __future__ import annotations  # https://www.python.org/dev/peps/pep-0563/

import ast
from dataclasses import dataclass
from functools import total_ordering
from typing import Union


@dataclass
@total_ordering
class Location:
    file: str
    line: int
    column: int

    def __eq__(self, other: Location) -> bool:
        return self.file == other.file and self.line == other.line and self.column == other.column

    def __lt__(self, other: Location) -> bool:
        return self.file < other.file or self.line < other.line or self.column < other.line

    def __str__(self) -> str:
        return f"'{self.file}' ({self.line}:{self.column})"

    @staticmethod
    def create_location(file: str, node: Union[ast.stmt, ast.expr]) -> Location:
        return Location(file, node.lineno, node.col_offset)
