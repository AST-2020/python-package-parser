import json


class Structure:
    def __init__(self):
        self.dict = {'method': {}, 'function': {}, 'package__all__list': {}}
        self.cls_name = None
        self.module_path = None
        self.list__all__ = False
        self.import_list = []

    def add_class_path(self, cls_path):
        self.dict['method'][cls_path] = {}

    def add_class_name(self, cls_path, cls_name):
        self.dict['method'][cls_path][cls_name] = {}

    def add_method(self, cls_path, cls_name, method, params):
        self.dict['method'][cls_path][cls_name][method] = params

    def add_module(self, module_pth):
        self.dict['function'][module_pth] = {}

    def add_func(self, module_pth, func_name, params):
        self.dict['function'][module_pth][func_name] = params

    def add__all__(self, module_path, modules):
        self.dict['package__all__list'][module_path] = []
        self.dict['package__all__list'][module_path] = modules

    # convert data into Json format
    def toJSON(self):
        return json.dumps(self.dict, default=lambda o: o.__dict__,
                          sort_keys=True, indent=3)
