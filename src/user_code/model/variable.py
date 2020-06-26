
class Variable:

    def __init__(self, name ,lineno , value):
        self.name = name
        self.lineno = lineno
        self.value = value
        self.type = type(value)

    def set_type(self, type):
        self.type = type

    def get_type(self):
        return self.type



    def print_variable(self):
        print(self.name, ': ', self.lineno,': ', self.value,': ' ,self.type)
if __name__ == '__main__':
    var = Variable('N', 13 , 64)
    var2 = Variable('D_in', 13 , 1000)
    var3 = Variable('H', 13, 100)
    var4 = Variable('D_out', 13, 10)
    var5 = Variable('N', 20, 3)

    vars = []
    vars.append(var)
    vars.append(var2)
    vars.append(var3)
    vars.append(var4)
    vars.append(var5)

    for var in vars:
        var.print_variable()

    for var in vars:
        if 'N' == var.name:
            var.print_variable()

