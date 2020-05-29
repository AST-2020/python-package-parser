

class UsedVariables:
    def __init__(self):
        self.dict = {}

    def add_variable(self, var):
        if var not in self.dict.keys():
            self.dict[var] = {}

    def add_usage(self, var, line, type):
        if var not in self.dict.keys():
            self.add_variable(var)
        self.dict[var][line] = type

    def get_var_type(self, var, line):
        # get latest declaration seen from current line
        if var in self.dict.keys():
            maxl = 0
            for ln in self.dict[var]:
                if maxl < ln <= line:
                    maxl = ln
            return self.dict[var][maxl]
        return None
