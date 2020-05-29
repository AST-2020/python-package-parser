class testFile1:
    def __init__(self, name, nachname="yoyoyo"):
        print(64486)


class testFile2:
    def __init__(self, name2=None):
        pass


obj1 = testFile1()


def testFunc1(num, my_list=[], my_bool=True, my_double=1.4, my_obj=obj1):
    print("hello")


def testFunc2(num={}, num2=2):
    print("hello")
