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

        match = re.match("^[Ll]ist\\[(.*)]$", s)
        if match is not None:
            matches = find_obj_for_str_parts(match)
            return find_obj_type_hint("Tuple", matches)

        matches = re.match("^[Tt]uple\\[(.*)]$", s)
        if matches is not None:
            matches = find_obj_for_str_parts(matches)
            return find_obj_type_hint("Tuple", matches)

        matches = re.match("^[Dd]ict\\[(.*)]$", s)
        if matches is not None:
            matches = find_obj_for_str_parts(matches)
            return find_obj_type_hint("Dict", matches)

        matches = re.match("^[Cc]allable\\[(.*)]$", s)
        if matches is not None:
            matches = find_obj_for_callable_parts(matches)
            if matches[0] == Ellipsis:
                matches[1] = remove_illegal_types(matches[1])
                return eval("Callable[[ellipsis]," + matches[1] + "]")
            else:
                print("Callable[[" + matches[0] + "]," + matches[1] + "]")
                result = ''
                for element in matches[0]:
                    result += str(element)
                result = result.replace("'", "")
                print(result)
                return eval("Callable[" + result + "," + matches[1] + "]")

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


def find_obj_for_callable_parts(matches):
    matches = matches.group(1).split(", ")
    matches = correct_splitting(matches)
    if matches[0][0] == "[" and matches[0][-1] == "]":
        matches[0] = matches[0][1: -1]
    matches[0] = correct_splitting(matches[0].split(", "))
    matches[0] = list(map(convert_string_to_type, matches[0]))
    matches[1] = correct_splitting(matches[1].split(", "))
    matches[1] = list(map(convert_string_to_type, matches[1]))
    for i in range(len(matches[0])):
        matches[0][i] = remove_illegal_types(matches[0][i].__str__())

    matches[1] = matches[1].__str__().rsplit("]", 1)[0].split("[", 1)[1]
    matches[1] = remove_illegal_types(matches[1])
    return [matches[0].__str__(), matches[1].__str__()]


def find_obj_for_str_parts(matches):
    matches = matches.group(1).split(", ")
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
