n = 0


class testFile1:
    def __init__(self, name, nachname="yoyoyo"):
        pass


class testFile2:
    def __init__(self, name2=None):
        pass


obj1 = testFile1()


def testFunc1(num, my_list=[], my_bool=True, my_double=1.4, my_obj=obj1) -> int:
    print("hello")


def testFunc2(num={}, num2=2):
    print("hello")


if True:
    def testFunc10(same_arg, not_same):
        pass
elif n == 1:
    def testFunc10(same_arg, really_different):
        pass
else:
    def testFunc10(same_arg, else_different):
        pass