from typing import List, Dict, TypeVar

T = TypeVar('T')


def _dict_to_list(dct: Dict) -> List[T]:
    if dct is None:
        return None
    return list(dct.values())


def _list_to_dict(lst: List[T]) -> Dict[str, T]:
    if lst is not None:
        return {element.get_name(): element for element in lst}
    else:
        return None
