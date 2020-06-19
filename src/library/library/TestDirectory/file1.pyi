from typing import List


# class testFile2:
#     def __init__(self, hint: Tuple[Tensor, Tensor], name2:Optional[Callable[[], float]]):
#         pass

class testFile2:
    def __init__(self, hint: Optional[Callable[[], float]], name2):
        pass
    # hint: Optional[Callable[[], float]]

    # hint: Optional[Callable[, float]]



def testFunc1(num: str ="yoyoyo", my_list: List=[], my_bool: bool=True, my_double: Double=1.4, my_obj=obj1) -> int:
    pass

@overload
def testFunc1(num: string ="yoyoyo", my_list: Dict=[], my_bool: boolean=True, my_double=1.4, my_obj: real=obj1) -> int:
    pass