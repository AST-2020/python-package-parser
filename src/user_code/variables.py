"""
UsedVariables stores declared variables, where only variables with type annotations are seen,
and saves the line of declaration and type for the variable.
"""


class UsedVariables:
    def __init__(self):
        self.dict = {}

    # add a variable name
    def add_variable(self, var):
        if var not in self.dict.keys():
            self.dict[var] = {}

    # add when a variable is declared and how
    def add_usage(self, var, line, type):
        if var not in self.dict.keys():
            self.add_variable(var)
        self.dict[var][line] = type

    # get the latest type of var before it is used in line
    def get_var_type(self, var, line):
        if var in self.dict.keys():
            maxl = 0
            for ln in self.dict[var]:
                if maxl < ln <= line:
                    maxl = ln
            return self.dict[var][maxl]
        return None
