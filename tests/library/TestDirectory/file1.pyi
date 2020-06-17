from typing import List, Dict, overload


# class testFile1:
#     def __init__(self, name: Tuple[Tensor, Tensor], nachname:str):
#         pass

def testFunc1(num:str, my_list:List, my_bool:bool, my_double:Float, my_obj:obj) -> int:
    print("hello")

@overload
def testFunc1(num:str, my_list:Dict, my_bool:boolean, my_double:Double, my_obj:obj) -> int:
    print("hello")

def testFunc1(my_list:List, my_bool:bool, my_double:Float, my_obj:obj) -> int:
    print("hello")


# def testFunc2(num:Dict, num2):
#     print("hello")
