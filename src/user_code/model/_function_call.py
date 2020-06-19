from typing import List

from library.model import Function
from user_code.model._location import Location
from user_code.model.argument import Arg, Kw_arg

class FunctionCall:
    def __init__(self, name: str, number_of_positional_args: int, positional_arg:List[Arg], keyword_arg:List[Kw_arg] ,keyword_arg_names: List[str],
                 callee_candidates: List[Function], location: Location):
        self.name: str = name
        self.number_of_positional_args: int = number_of_positional_args
        self.positional_arg: List[Arg] = positional_arg #--
        self.keyword_arg : List[Kw_arg] = keyword_arg #--
        self.keyword_arg_names: List[str] = keyword_arg_names
        self.callee_candidates: List[Function] = callee_candidates
        self.location: Location = location
