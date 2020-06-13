from typing import Dict, List

from ._function import Function
from ._klass import Class
from ._util import _dict_to_list


class Module:
    def __init__(self, name: str):
        self.__name: str = name
        self.__classes: Dict[str, List[Class]] = {}
        self.__top_level_functions: Dict[str, List[Function]] = {}

    def get_name(self) -> str:
        return self.__name

    def add_class(self, klass: Class):
        if klass.get_name() not in self.__classes:
            self.__classes[klass.get_name()] = []

        self.__classes[klass.get_name()].append(klass)

    def get_classes_with_name(self, class_name: str) -> List[Class]:
        return self.__classes.get(class_name, [])

    def get_all_classes(self) -> List[Class]:
        result = []
        for classesWithSameName in _dict_to_list(self.__classes):
            result += classesWithSameName
        return result

    def add_top_level_function(self, function: Function):
        if function.get_name() not in self.__top_level_functions:
            self.__top_level_functions[function.get_name()] = []

        self.__top_level_functions[function.get_name()].append(function)

    def get_top_level_functions_with_name(self, function_name: str) -> List[Function]:
        return self.__top_level_functions.get(function_name, [])

    def get_all_top_level_functions(self) -> List[Function]:
        result = []
        for functionsWithSameName in _dict_to_list(self.__top_level_functions):
            result += functionsWithSameName
        return result
