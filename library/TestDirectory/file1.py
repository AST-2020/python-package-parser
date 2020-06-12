from typing import List


class testFile1:
    def __init__(self, name, nachname="yoyoyo"):
        pass


class testFile2:
    def __init__(self, name2=None):
        pass


obj1 = testFile1()


def testFunc1(num, my_list: List, my_bool: bool=True, my_double: float=1.4, my_obj: testFile1=obj1) -> int:
    '''
    :arguidsbvfsdkj
        nvjodfvnfdsl
    '''
    print("hello")


def testFunc2(num={}, num2=2):
    print("hello")
