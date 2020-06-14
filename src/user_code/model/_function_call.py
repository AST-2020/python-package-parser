from typing import List

from library.model import Function
from user_code.model._location import Location


class FunctionCall:
    def __init__(self, name: str, number_of_positional_args: int, keyword_arg_names: List[str], location: Location,
                 callee_candidates: List[Function]):
        self.name: str = name
        self.number_of_positional_args: int = number_of_positional_args
        self.keyword_arg_names: List[str] = keyword_arg_names
        self.location: Location = location
        self.callee_candidates: List[Function] = callee_candidates
