import json


class Structure:
    def __init__(self):
        self.dict = {'method': {}, 'function': {}}
        self.cls_name = None


    def add_class(self, cls_name):
        self.dict['method'][cls_name] = {}

    def add_path(self, path):
        self.dict['function'][path] = {}


    def add_method(self, cls, method, params):
        self.dict['method'][cls][method] = params

    def add_func(self, path, func_name, params):
        self.dict['function'][path][func_name] = params


    # json as storage solution
    def save(self, file):
        with open(file, 'w') as outfile:
            json.dump(self.dict, outfile, indent=4)
        # print('Data saved to json file.')

    def load(self, file):
        with open(file) as inputfile:
            self.dict = json.load(inputfile)
