from typing import List, Dict, overload, Tuple, Callable, Optional

# my_list = [List, Dict, overload, "Tuple", "Callable", "Optional"]

class testFile1:
    def __init__(self, name: List[Tensor, str], nachname:str):
        # if __name__ == '__main__':
        #     s = "List[..."
        #     convert_str_to_obj()
        #     obj_type = List...
        #     eval("List[Tensor]") #

        pass

def testFunc1(num:str, my_list:List, my_bool:bool, my_double:Float, my_obj:obj) -> int:
    pass

@overload
def testFunc1(num:str, my_list:Dict, my_bool:boolean, my_double:Double, my_obj:obj) -> int:
    pass
#
# def testFunc1(my_list:List, my_bool:bool, my_double:Float, my_obj:obj) -> int:
#     pass


# def testFunc2(num:Dict, num2):
#     pass
