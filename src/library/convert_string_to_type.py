import re
from typing import *
from torch import Tensor


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

        match = re.match("^[Oo]ptional\\[(.*)]$", s)  # Optional[X] as a shorthand for Union[X, None]
        if match is not None:
            return Optional[convert_string_to_type(match.group(1))]

        matches = re.match("^[Uu]nion\\[(.*)]$", s)
        if matches is not None:
            matches = matches.group(1).split(", ")
            matches = list(map(convert_string_to_type, matches))
            unions = matches[0]
            for i in range(1, len(matches)):
                unions = Union[unions, matches[i]]
            return unions

        matches = re.match("^[Tt]uple\\[(.*)]$", s)
        if matches is not None:
            n = 0
            index = 0
            matches = matches.group(1).split(", ")
            while index < len(matches):
                for chary in matches[index]:
                    if chary == "[":
                        n += 1
                    elif chary == "]":
                        n -= 1
                if n != 0:
                    while n != 0:
                        n = merge_strings(n, matches[index + 1])
                        matches[index] += ", " + matches[index + 1]
                        del matches[index + 1]
                index += 1
            matches = list(map(convert_string_to_type, matches))
            unions = Tuple[matches]
            return unions
        # Tuple[List[Callable[[int], float]], str, float, obj]

        matches = re.match("^[Dd]ict\\[(.*)]$", s)
        if matches is not None:
            matches = matches.group(1).split(", ")
            return Dict[convert_string_to_type(matches[0]), convert_string_to_type(matches[1])]

        match = re.match("^[Cc]allable\\[\\[(.*)]$", s)
        if match is None:
            match = re.match("^[Cc]allable\\[(.*)]$", s)
        if match is not None:
            match = match.group(1).rsplit("], ")
            if len(match) == 1:
                match = match[0].rsplit(", ")
            match1 = match[0].split(", ")
            match1 = list(map(convert_string_to_type, match1))
            match2 = convert_string_to_type(match[1])
            return Callable[match1, match2]
        return Any

def merge_strings(n:int, hint: str):
    for chary in hint:
        if chary == "[":
            n +=1
        elif chary == "]":
            n -= 1
    return n

