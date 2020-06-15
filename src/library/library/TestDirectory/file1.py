from typing import Tuple

from tensorflow import Tensor


class testFile1:
    def __init__(self, name, nachname="yoyoyo"):
        pass


class testFile2:
    def __init__(self, hint: Tuple[Tensor, Tensor], name2=None):
        pass


obj1 = testFile1()


def testFunc1(num="yoyoyo", my_list=[], my_bool=True, my_double=1.4, my_obj=obj1) -> int:
    print("hello")


def testFunc2(num={}, num2=2):
    print("hello")
