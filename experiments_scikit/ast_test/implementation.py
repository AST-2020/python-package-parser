class Structure:
    def __init__(self):
        self.dict = {}
        self.cls_name = None

    # to be honest i don't even know, if we need to add the names of the classes

    # def add_class(self, cls_name):
    #    'self.dict[cls_name] = {}'

    def add_func(self, func_name, cls_name):
        if cls_name is None:
            self.dict[func_name] = []
        else:
            self.dict[cls_name][func_name] = []
