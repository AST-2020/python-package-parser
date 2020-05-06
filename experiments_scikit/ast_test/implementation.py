import json


class Structure:
    def __init__(self):
        self.dict = {"global_func": {}}
        self.cls_name = None

    def add_class(self, cls_name):
        self.dict[cls_name] = {}

    def add_func(self, func_name, cls_name):
        if cls_name is None:
            # now we save all functions that are not in a class, under the key global_func
            self.dict["global_func"][func_name] = []
        else:
            self.dict[cls_name][func_name] = []

    # convert data into Json format
    def toJSON(self):
        return json.dumps(self.dict, default=lambda o: o.__dict__,
                          sort_keys=True, indent=3)
