import re
from typing import *
import typing
from torch import Tensor


def convert_string_to_type(s: str) -> Type:
    try:
        if "ellipsis" in s:
            s = s.replace("ellipsis", "...")
        return eval(s)
    except (NameError, SyntaxError, TypeError) as e:
        if s == "string":
            return str
        elif s == "boolean":
            return bool
        elif s == "Integer" or s == "integer":
            return int
        elif s == 'None' or s == 'none':
            return None

        match = re.match("^(.*?)\\[(.*)]$", s)
        if match is not None:
            match = re.match("^(.*?)\\[(.*)]$", s).group(1)
            match = match.capitalize()  # bec. in doc_strings, some types begin with small letters
            match2 = re.match("^(.*?)\\[(.*)]$", s).group(2)
            matches = find_obj_for_str_parts(match2)
            return find_obj_type_hint(match, matches)
        return Any


def calculate_n(hint: str):
    return hint.count("[") - hint.count("]") + hint.count("(") - hint.count(")")


# to check if splitting using "," only was correct or not
def correct_splitting(matches):
    index = 0
    try:
        while index < len(matches):
            n = calculate_n(matches[index])
            while n != 0:
                # concatenate string_part with the next one in List
                # ex: ["List[int,", "str]"] -> "List[int, str]" (which is what we want)
                matches[index] += ", " + matches.pop(index + 1)
                n = calculate_n(matches[index])
            index += 1
        return matches
    except IndexError:
        return Any


def find_obj_for_str_parts(matches):
    matches = matches.split(", ")
    matches = correct_splitting(matches)
    matches = list(map(convert_string_to_type, matches))
    return matches


def find_obj_type_hint(outer_type, matches):
    matches = matches.__str__().rsplit("]", 1)[0].split("[", 1)[1]
    matches = remove_illegal_types(matches)
    try:
        return eval(outer_type + "[" + matches + "]")
    except NameError:
        return Any


def remove_illegal_types(s):
    return s.replace("<class '", "").replace("'>", "").replace("NoneType", "None").replace("torch.Tensor", "Tensor").\
        replace("<built-in function ", "").replace(">", "")
