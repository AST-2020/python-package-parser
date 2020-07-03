import re
from typing import *
from torch import Tensor

# union and optional will not be handled in the except part (meaning if the whole expression included is not composed of
# types that we support), as type_hints of the form (Optional[typing.any]) or (Union[typing.any, ...])


def convert_string_to_type(s: str) -> Type:
    try:
        if "ellipsis" in s:
            s = s.replace("ellipsis", "...")
        return eval(s)
    except (NameError, SyntaxError) as e:
        if s == "string" or s == "str":
            return str
        if s == "boolean":
            return bool
        if s == "Integer" or s == "integer":
            return int

        match = re.match("^[Ll]ist\\[(.*)]$", s)
        if match is not None:
            return List[convert_string_to_type(match.group(1))]

        matches = re.match("^[Dd]ict\\[(.*)]$", s)
        if matches is not None:
            matches = matches.group(1).split(", ")
            return Dict[convert_string_to_type(matches[0]), convert_string_to_type(matches[1])]

        matches = re.match("^[Tt]uple\\[(.*)]$", s)
        if matches is not None:
            matches = matches.group(1).split(", ")
            matches = correct_splitting(matches)
            matches = list(map(convert_string_to_type, matches))
            unions = Tuple[matches]
            return unions

        match = re.match("^[Cc]allable\\[\\[(.*)]$", s)
        if match is None:
            match = re.match("^[Cc]allable\\[(.*)]$", s)
        if match is not None:
            match = match.group(1).rsplit("], ")
            if len(match) == 1:
                match = match[0].rsplit(", ")
            match1 = match[0].split(", ")
            match1 = correct_splitting(match1)
            match1 = list(map(convert_string_to_type, match1))
            match2 = convert_string_to_type(match[1])
            return Callable[match1, match2]
        return Any


def calculate_n(n: int, hint: str):
    return n + hint.count("[") - hint.count("]")


def correct_splitting(matches):
    index = 0
    while index < len(matches):
        n = calculate_n(0, matches[index])
        while n != 0:
            # concatenate string_part with the next one in List
            # ex: ["List[int,", "str]"] -> "List[int, str]" (which is what we want)
            matches[index] += ", " + matches.pop(index + 1)
            n = calculate_n(n, matches[index + 1])
        index += 1
        return matches



