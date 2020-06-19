import re
from typing import *


def convert_string_to_type(s: str) -> Type:
    try:
        return eval(s)
    except NameError:
        if s == "string":
            return str
        if s == "boolean":
            return bool

        match = re.match("^List\[(.*)]$", s)
        if match is not None:
            return List[convert_string_to_type(match.group(1))]

        return Any
