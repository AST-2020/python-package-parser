import json
from typing import List

# 2 get methods have been added
# get_args() is recommended to be used when trying to access parts of the parsed data

class Structure:
    def __init__(self):
        self.dict = {'method': {}, 'function': {}, 'package__all__list': {}}
        self.cls_name = None
        self.module_path = None
        self.list__all__ = False
        self.import_list = []

    def get(self, data, path: List):
        if len(path) == 0:
            return data
        if (isinstance(data, list) or isinstance(data, dict)) and path[0] in data:
            return self.get(data[path[0]], path[1:])
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
        if self.get(self.dict, ["method", module_path]) is None:
            self.add_module_path("method", module_path)

        if self.get(self.dict, ["method", module_path, cls_name]) is None:
            self.add_class_name(module_path, cls_name)

        self.dict['method'][module_path][cls_name][method] = params

    def add_func(self, module_path, func_name, params):
        if self.get(self.dict, ["function", module_path]) is None:
            self.add_module_path("function", module_path)
        self.dict['function'][module_path][func_name] = params

    def add__all__(self, module_path, modules):
        self.dict['package__all__list'][module_path] = []
        self.dict['package__all__list'][module_path] = modules

    # to get the arguments for functions and methods
    def get_args(self, structure, path_till_file, func_or_method_name, cls_name=None):
        if cls_name is None:
            return self.get(structure, ["function", path_till_file, func_or_method_name])
        else:
            return self.get(structure, ["method", path_till_file, cls_name, func_or_method_name])

    # convert data into Json format
    # should be deleted, if nobody is already using it
    # (convert_to_json) is better
    def toJSON(self, structure):
        return json.dumps(structure, default=lambda o: o.__dict__,
                          sort_keys=True, indent=3)

    def convert_to_json(self, package_name):
        json_object = json.dumps(self.dict, default=lambda o: o.__dict__,
                                 sort_keys=True, indent=3)
        # print(json_object)
        with open("results_" + package_name + ".txt", 'w') as outfile:
            json.dump(json_object, outfile)
        print("Package " + package_name + " has been successfully parsed")

    # ex data_file_path = 'testTextFile.txt'
    def convert_to_python(self, data_file_path):
        with open(data_file_path) as json_file:
            python_data = json.load(json_file)
        self.dict = json.loads(python_data)
        print(self.dict)
