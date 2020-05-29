import json
from typing import List


# 2 get methods have been added
# get_args() is recommended to be used when trying to access parts of the parsed data

class Parameter:
    def __init__(self, param_name, has_default=False, default_value=None):
        self.param_name = param_name
        self.has_default = has_default
        self.default_value = default_value


class Function:
    def __init__(self, params: List[Parameter]) :
        self.params = params


class Structure:
    def __init__(self):
        self.dict = {'method': {}, 'function': {}, 'package__all__list': {}}
        self.cls_name = None
        self.module_path = None
        self.list__all__ = False
        self.import_list = []

    def __get(self, data, path: List):
        if len(path) == 0:
            return data
        if (isinstance(data, list) or isinstance(data, dict)) and path[0] in data:
            return self.__get(data[path[0]], path[1:])
        else:
            return None

    def add_module_path(self, func_or_method, module_path):
        if func_or_method is "function":
            self.dict['function'][module_path] = {}
        elif func_or_method is "method":
            self.dict['method'][module_path] = {}

    def add_class_name(self, module_path, cls_name):
        self.dict['method'][module_path][cls_name] = {}

    def add_method(self, module_path, cls_name, method, params):
        params_as_object = [self.create_params_object(param) for param in params]
        function = Function(params_as_object)
        if self.__get(self.dict, ["method", module_path]) is None:
            self.add_module_path("method", module_path)

        if self.__get(self.dict, ["method", module_path, cls_name]) is None:
            self.add_class_name(module_path, cls_name)
        self.dict['method'][module_path][cls_name][method] = function

    def add_func(self, module_path, func_name, params):
        params_as_object = [self.create_params_object(param) for param in params]
        function = Function(params_as_object)
        if self.__get(self.dict, ["function", module_path]) is None:
            self.add_module_path("function", module_path)
        self.dict['function'][module_path][func_name] = function

    def create_params_object(self, param):
        if len(param) == 1:
            return Parameter(param[0])
        elif len(param) == 2:
            return Parameter(param[0], True, param[1])
        else:
            raise ValueError("parameter should have lenght between 1 and 2")

    def add__all__(self, module_path, modules):
        self.dict['package__all__list'][module_path] = []
        self.dict['package__all__list'][module_path] = modules

    def get_classes(self, path_till_file) -> List:
        return self.__get(self.dict, ["method", path_till_file]).keys()

    def get_functions_or_methods(self, path_till_file, cls_name=None):
        if cls_name is None:
            return self.__get(self.dict, ["function", path_till_file])
        else:
            return self.__get(self.dict, ["method", path_till_file, cls_name])

    # to get the arguments for functions and methods
    def get_args(self, path_till_file, func_or_method_name, cls_name=None):
        if cls_name is None:
            return self.__get(self.dict, ["function", path_till_file, func_or_method_name])
        else:
            return self.__get(self.dict, ["method", path_till_file, cls_name, func_or_method_name])

    def get_args_names(self):
        pass

    def get_imports_from_all(self, path):
        return self.__get("package__all__list", path)

    # convert data into Json format
    def convert_to_json(self, package_name):
        json_object = json.dumps(self.dict, default=lambda o: o.__dict__, sort_keys=True, indent=3)
        print(json_object)
        with open("results_" + package_name + ".json", 'w') as outfile:
            json.dump(json_object, outfile)
        print("Package " + package_name + " has been successfully parsed")

    # ex data_file_path = 'testTextFile.txt'
    def convert_to_python(self, data_file_path):
        with open(data_file_path) as json_file:
            python_data = json.load(json_file)
        self.dict = json.loads(python_data)
        print(self.dict)


