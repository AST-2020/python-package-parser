from typing import Dict, List, Optional

from ._parameter import Parameter
from ._util import _dict_to_list, _list_to_dict


class Function:
    def __init__(self, name: str, parameters: List[Parameter]):
        self.__name: str = name
        self.__parameters: Dict[str, Parameter] = _list_to_dict(parameters)

    def get_name(self) -> str:
        return self.__name

    def get_parameter(self, parameter_name: str) -> Optional[Parameter]:
        return self.__parameters.get(parameter_name)

    def get_parameters(self) -> List[Parameter]:
        return _dict_to_list(self.__parameters)

    def __str__(self) -> str:
        if self.__parameters is not None:
            parameter_string = ", ".join(self.__parameters)
        else:
            parameter_string = "None"
        return f"def {self.__name}({parameter_string})"
