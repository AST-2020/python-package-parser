from typing import Dict, List, Optional

from ._klass import Class
from ._function import Function
from ._module import Module
from ._util import _dict_to_list, _list_to_dict


class Package:
    def __init__(self, name: str, modules: List[Module] = None):
        if modules is None:
            modules = []

        self.__name: str = name
        self.__modules: Dict[str, Module] = _list_to_dict(modules)

    def get_name(self) -> str:
        return self.__name

    def add_module(self, module: Module):
        if module.get_name() in self.__modules:
            raise RuntimeError(f"Dictionary already contains an element with name {module.get_name()}.")

        self.__modules[module.get_name()] = module

    def get_module(self, module_path: str) -> Optional[Module]:
        return self.__modules.get(module_path)

    def get_all_modules(self) -> List[Module]:
        return _dict_to_list(self.__modules)

    # Helper getters for easier access across multiple levels of the object structure

    def get_classes_with_name(self, module_path: str, class_name: str) -> List[Class]:
        module = self.get_module(module_path)
        if module is None:
            return []

        return module.get_classes_with_name(class_name)

    def get_methods_with_name(self, module_path: str, class_name: str, method_name: str) -> List[Function]:
        classes = self.get_classes_with_name(module_path, class_name)
        if classes is None:
            return []

        result = []
        for klass in classes:
            result += klass.get_methods_with_name(method_name)
        return result

    def get_top_level_functions_with_name(self, module_path: str, function_name: str) -> List[Function]:
        module = self.get_module(module_path)
        if module is None:
            return []

        return module.get_top_level_functions_with_name(function_name)
