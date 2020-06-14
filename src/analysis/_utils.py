from typing import Optional, List

from library.model import Parameter, Function


def get_parameters(callee_candidates: List[Function]) -> Optional[List[Parameter]]:
    if len(callee_candidates) != 1:
        return None
    else:
        return callee_candidates[0].get_parameters()
