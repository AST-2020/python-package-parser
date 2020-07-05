from typing import *
from torch import Tensor


#
#
# class testFile5:
#     def __init__(self, name, nachname, echte_name):
#         pass
#
#     def method_50(self, num, my_list, my_bool, my_double, stringy, my_obj) -> int:
#         pass
#
#     def method_51(self, name, nachname, echte_name):
#         pass
#
#     if True:
#         def method_52(self, name, nachname, echte_name):
#             pass
#     else:
#         def method_52(self, name2: int, nachname2, echte_name2):
#             pass
#
#     def method_53(self, name, nachname: str="yoyoyo", echte_name="kein Witz"):
#         pass
#
#
# obj = testFile5()
#
#
# def testFunc51(num, my_list, my_bool, my_double, my_obj):
#     pass
#

# def testFunc52(arg0: Dict, arg1: Tuple[List[Callable[[int], float]], device],
#                arg2: Tuple[List[Callable[[int], float]], Tensor], arg3:Callable[..., device]):
#     pass
# def testFunc52(arg0: Dict, arg1: Tuple[int, Tensor], arg2: Tuple[List[Callable[[int], float]], str, float, obj],
#                arg3:Callable[[Tuple[int, Exception, device]], None]):
# def testFunc52(arg0, arg1, arg2,
#                arg3:Callable[[Tuple[int, Exception, device], device], device]):
def testFunc52(arg0, arg1, arg2,
                   arg3: Callable[[Tuple[int, Exception, device], device], int]):
    pass
