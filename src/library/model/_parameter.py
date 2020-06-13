from typing import Any


class Parameter:
    def __init__(self, name: str, type_hint: Any = None, has_default: bool = False, default: Any = None):
        self.__name: str = name
        self.__type_hint__: Any = type_hint
        self.__has_default: bool = has_default
        self.__default: Any = default

    def get_name(self) -> str:
        return self.__name

    def get_type_hint(self) -> Any:
        return self.__type_hint__

    def has_default(self) -> bool:
        return self.__has_default

    def get_default(self) -> Any:
        return self.__default

    def __str__(self) -> str:
        result = self.__name
        if self.__type_hint__ is not None:
            result += f": {self.__type_hint__}"
        if self.__has_default:
            result += f" = {self.__default}"
        return result
