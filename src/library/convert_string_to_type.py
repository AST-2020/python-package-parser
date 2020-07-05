import re
from typing import *

import typing
from torch import Tensor

# union and optional will not be handled in the except part (meaning if the whole expression included is not composed of
# types that we support), as type_hints of the form (Optional[typing.any]) or (Union[typing.any, ...])


# use the second approach: which returns only the name of the type, ex: 'Dict' instead of 'Dict[typing.Any, int]'
# reasons:
# 1- with really big inputs ,like in dictionaries for example, we will probably not go through all the key-value-pair
#     which can be in the millions, espicially if one of them is typing.Any
#     counter argument: program will take really long, so why not wait a couple of minutes to figure our errors

def convert_string_to_type(s: str) -> Type:
    try:
        if "ellipsis" in s:
            s = s.replace("ellipsis", "...")
        return eval(s)
    except (NameError, SyntaxError) as e:
        if s == "string" or s == "str":
            return str
        elif s == "boolean":
            return bool
        elif s == "Integer" or s == "integer":
            return int

        match = re.match("^(.*?)\\[(.*)]$", s)
        if match is not None:
            match = re.match("^(.*?)\\[(.*)]$", s).group(1)
            match2 = re.match("^(.*?)\\[(.*)]$", s).group(2)
            matches = find_obj_for_str_parts(match2)
            return find_obj_type_hint(match, matches)

        return Any


def calculate_n(hint: str):
    return hint.count("[") - hint.count("]")


# to check if splitting using "," only was correct or not
def correct_splitting(matches):
    index = 0
    while index < len(matches):
        n = calculate_n(matches[index])
        while n != 0:
            # concatenate string_part with the next one in List
            # ex: ["List[int,", "str]"] -> "List[int, str]" (which is what we want)
            matches[index] += ", " + matches.pop(index + 1)
            n = calculate_n(matches[index])
        index += 1
        return matches


def find_obj_for_str_parts(matches):
    matches = matches.split(", ")
    matches = correct_splitting(matches)
    matches = list(map(convert_string_to_type, matches))
    return matches


def find_obj_type_hint(outer_type, matches):
    matches = matches.__str__().rsplit("]", 1)[0].split("[", 1)[1]
    matches = remove_illegal_types(matches)
    return eval(outer_type + "[" + matches + "]")


def remove_illegal_types(s):
    return s.replace("<class '", "").replace("'>", "")

# 'Tuple[List[Callable[[int], float]], device]'
