from typing import Dict, List

from ._function import Function
from ._util import _dict_to_list, _list_to_dict


class Class:
    def __init__(self, name: str, methods: List[Function] = None):
        if methods is None:
            methods = []

        self.__name: str = name
        self.__methods: Dict[str, List[Function]] = _list_to_dict(methods)

    def get_name(self) -> str:
        return self.__name

    def add_method(self, method: Function):
        if method.get_name() not in self.__methods:
            self.__methods[method.get_name()] = []

        self.__methods[method.get_name()].append(method)

    def get_methods_with_name(self, method_name: str) -> List[Function]:
        return self.__methods.get(method_name, [])

    def get_all_methods(self) -> List[Function]:
        result = []
        for methodsWithSameName in _dict_to_list(self.__methods):
            result += methodsWithSameName
        return result

    def __str__(self) -> str:
        return f"class {self.__name}"
