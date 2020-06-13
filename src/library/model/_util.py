from typing import List, Dict, TypeVar

T = TypeVar('T')


def _dict_to_list(dct: Dict) -> List[T]:
    return list(dct.values())


def _list_to_dict(lst: List[T]) -> Dict[str, T]:
    return {element.get_name(): element for element in lst}
