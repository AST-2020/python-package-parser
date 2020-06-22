import re
from typing import *
from torch import Tensor


def convert_string_to_type(s: str) -> Type:
    try:
        return eval(s)
    except (NameError, SyntaxError, TypeError) as e:
        if s == "string" or s == "str":
            return str
        if s == "boolean":
            return bool

        match = re.match("^List\\[(.*)]$", s)
        if match is not None:
            return List[convert_string_to_type(match.group(1))]

        match = re.match("^Optional\\[(.*)]$", s)  # Optional[X] as a shorthand for Union[X, None]
        if match is not None:
            return Optional[convert_string_to_type(match.group(1))]

        matches = re.match("^Union\\[(.*)]$", s)
        if matches is not None:
            matches = matches.group(1).split(", ")
            matches = list(map(convert_string_to_type, matches))
            unions = matches[0]
            for i in range(1, len(matches)):
                unions = Union[unions, matches[i]]
            return unions

        matches = re.match("^Tuple\\[(.*)]$", s)
        if matches is not None:
            matches = matches.group(1).split(", ")
            matches = list(map(convert_string_to_type, matches))
            unions = matches[0]
            for i in range(1, len(matches)):
                unions = Tuple[unions, matches[i]]
            return unions

        matches = re.match("^Dict\\[(.*)]$", s)
        if matches is not None:
            matches = matches.group(1).split(", ")
            return Dict[convert_string_to_type(matches[0]), convert_string_to_type(matches[1])]

        match = re.match("^Callable\\[\\[(.*)]$", s)
        if match is None:
            match = re.match("^Callable\\[(.*)]$", s)
        if match is not None:
            match = match.group(1).rsplit("], ")
            if len(match) == 1:
                match = match[0].rsplit(", ")
            match1 = match[0].split(", ")
            match1 = list(map(convert_string_to_type, match1))
            match2 = list(map(convert_string_to_type, match[1]))
            return Callable[match1, match2[0]]

        return Any
