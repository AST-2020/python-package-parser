"""
structure for user_code arguments.
"""

class Arg:
    def __init__(self,value):
        self.value = value
        self.type = self.__set_typ(value)

    def __set_typ(self, value):
        # print(type(value))
        return type(value)
    def get_value(self):
        return self.value
    def get_type(self):
        return self.type

    def print_args(self):
            print(self.value, ':  ', self.type)


class Kw_arg(Arg):
    def __init__(self, name, value):
        self.name = name
        super().__init__(value)
    def print_kw_arg(self):
            print(self.name, self.value, ':  ', self.type)

class Arguments_of_function:
    def __init__(self):
        self.__function_name = ''
        self.__arg = []
        self.__kw_arg = []

    def add_arg(self,Arg: Arg):
        self.__arg.append(Arg)

    def add_kw_arg(self, kw_arg : Kw_arg):
        self.__kw_arg.append(kw_arg)

    def add_function_name(self,__function_name):
        self.__function_name = __function_name

    def print_all(self):
        print(self.__function_name)
        for a in range(len(self.__arg)):
            print(self.__arg[a].value, ':  ', self.__arg[a].type)
        for k in range(len(self.__kw_arg)):
            print(self.__kw_arg[k].name, ': ', self.__kw_arg[k].value, ': ', self.__kw_arg[k].type )

#f([1,2,3]



if __name__ == '__main__':

    n = 'hello world'
    arg = Argument()

    arg1 = Arg(n)
    arg2 = Arg('hello')
    arg3 = Arg(arg1)

    arg.add_arg(arg1)
    arg.add_arg(arg2)
    arg.add_arg(arg3)


    kwarg1 = Kw_arg('ggfgf', 5)
    kwarg2 = Kw_arg('wern', 8.2)
    kwarg3 = Kw_arg('b', {'i':1, 'f':2})
    kwarg4 = Kw_arg('ggfgf', arg2)

    arg.add_kw_arg(kwarg1)
    arg.add_kw_arg(kwarg2)
    arg.add_kw_arg(kwarg3)
    arg.add_kw_arg(kwarg4)

    arg.print_all()