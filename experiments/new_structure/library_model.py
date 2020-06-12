import json
from typing import List, Any, Dict, TypeVar, Optional


# ignore packages that don't have an __init__ module in them
# find out what are the uses for the __init__ file and when are the methods and functions there are invoked


# It will provide the same output as before, and don’t forget to remove the ‘()’ after func when printing it.
# Just writing @property above the function any_func() make it available to be used as a property.

class Parameter:
    def __init__(self, name: str, has_default: bool = False, default: Any = None):
        self.__name = name
        self.__has_default = has_default
        self.__default = default

    def get_name(self) -> str:
        return self.__name

    def has_default(self) -> bool:
        return self.__has_default

    def get_default(self) -> Any:
        return self.__default

    def __str__(self) -> str:
        if self.__has_default:
            return f"{self.__name} = {self.__default}"
        else:
            return self.__name


class Function:
    def __init__(self, name: str, parameters: List[Parameter]):
        self.__name = name
        self.__parameters = _list_to_dict(parameters)

    def get_name(self) -> str:
        return self.__name

    def get_parameter(self, parameter_name: str) -> Optional[Parameter]:
        return self.__parameters[parameter_name]

    def get_parameters(self) -> List[Parameter]:
        return _dict_to_list(self.__parameters)

    def __str__(self) -> str:
        parameter_string = ", ".join(self.__parameters)
        return f"def {self.__name}({parameter_string})"


class Class:
    def __init__(self, name: str, methods: List[Function]):
        self.__name = name
        self.__methods = _list_to_dict(methods)
        self.__to_ignore = []

    def add_to_ignore(self, method_name):
        self.__to_ignore.append(method_name)

    def get_to_ignore(self):
        return self.__to_ignore

    def get_name(self) -> str:
        return self.__name

    def add_method(self, method: Function):
        if method.get_name() not in self.get_to_ignore():
            if not _add_func_or_method_to_dict(self.__methods, method):
                self.add_to_ignore(method.get_name())

    def get_method(self, method_name: str) -> Optional[Function]:
        return self.__methods[method_name]

    def get_methods(self) -> List[Function]:
        return _dict_to_list(self.__methods)


class Module:
    def __init__(self, name: str, classes: List[Class], top_level_functions: List[Function]):
        self.__name = name
        self.__classes = _list_to_dict(classes)
        self.__top_level_functions = _list_to_dict(top_level_functions)
        self.__to_ignore = []

    def add_to_ignore(self, func_name):
        self.__to_ignore.append(func_name)

    def get_to_ignore(self):
        return self.__to_ignore

    def get_name(self) -> str:
        return self.__name

    def add_class(self, klass: Class):
        if klass.get_name() not in self.get_to_ignore():
            if not _add_class_to_dict(self.__classes, klass):
                self.add_to_ignore(klass.get_name())

    def get_class(self, class_name: str) -> Optional[Class]:
        return self.__classes[class_name]

    def get_classes(self) -> List[Class]:
        return _dict_to_list(self.__classes)

    def add_top_level_function(self, function: Function):
        if function.get_name() not in self.get_to_ignore():
            if not _add_func_or_method_to_dict(self.__top_level_functions, function):
                self.add_to_ignore(function.get_name())

    def get_top_level_function(self, function_name: str) -> Optional[Function]:
        return self.__top_level_functions[function_name]

    def get_top_level_functions(self) -> List[Function]:
        return _dict_to_list(self.__top_level_functions)


class Library:
    def __init__(self, modules: List[Module]):
        self.__modules = _list_to_dict(modules)
        self.__to_ignore = []

    def add_to_ignore(self, func_name):
        self.__to_ignore.append(func_name)

    def get_to_ignore(self):
        return self.__to_ignore

    def add_module(self, module: Module):
        _add_module_to_dict(self.__modules, module)

    def get_module(self, module_path: str) -> Optional[Module]:
        return self.__modules[module_path]

    def get_modules(self) -> List[Module]:
        return _dict_to_list(self.__modules)

    # Helper getters for easier access across multiple levels of the object structure

    def get_class(self, module_path: str, class_name: str) -> Optional[Class]:
        module = self.get_module(module_path)
        if module is None:
            return None

        return module.get_class(class_name)

    def get_method(self, module_path: str, class_name: str, method_name: str) -> Optional[Function]:
        klass = self.get_class(module_path, class_name)
        if klass is None:
            return None

        return klass.get_method(method_name)

    def get_top_level_function(self, module_path: str, function_name: str) -> Optional[Function]:
        module = self.get_module(module_path)
        if module is None:
            return None

        return module.get_top_level_function(function_name)

    # convert data into Json format
    def convert_to_json(self, package_name):
        # print(self.__modules)
        json_object = json.dumps(self.__modules, default=lambda o: o.__dict__, sort_keys=True, indent=3)
        print(json_object)
        with open("results_" + package_name + ".json", 'w') as outfile:
            json.dump(json_object, outfile)
        print("Package " + package_name + " has been successfully parsed")

    # ex data_file_path = 'testTextFile.txt'
    def convert_to_python(self, data_file_path):
        with open(data_file_path) as json_file:
            python_data = json.load(json_file)
        self.__modules = json.loads(python_data)


T = TypeVar('T')


def _dict_to_list(dct: Dict) -> List[T]:
    return [dct.keys()]


def _list_to_dict(lst: List[T]) -> Dict[str, T]:
    return {element.get_name(): element for element in lst}


def _add_module_to_dict(dct: Dict[str, T], element: T):
    if element.get_name() in dct:
        raise RuntimeError(f"Dictionary already contains an element with name {element.get_name()}.")
    dct[element.get_name()] = element


def _add_func_or_method_to_dict(dct, element: T) -> bool:
    if element.get_name() in dct:
        if element.get_parameters() != dct[element.get_name()].get_parameters():
            del dct[element.get_name()]
            return False
        return True
    else:
        dct[element.get_name()] = element
        return True


def _add_class_to_dict(dct, element: T) -> bool:
    if element.get_name() in dct:
        return False
    else:
        dct[element.get_name()] = element
        return True