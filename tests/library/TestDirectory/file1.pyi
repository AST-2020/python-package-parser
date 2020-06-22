from typing import List, Dict, overload, Tuple, Callable, Optional, Union, Any
from torch import Tensor

from library.model import Module


class testFile1:
    # def __init__(self, name: Optional[Union[_device, str, int]], nachname:Optional[int],
    #              echte_name:Callable[[Tensor, Tensor, int], Tensor]):
    # def __init__(self, name: Dict[float, _device], nachname:Callable[[Tensor, Tensor, int], Tensor],
    #              echte_name):
    # def __init__(self, name: Union[..., Tensor], nachname:Callable[[Tensor, Tensor, int], Tensor],
    #              echte_name:Callable[['Module'], None]):
    #     pass
    def __init__(self,
                 name:Union[Callable[[int], float], List[Callable[[int], float]]],
                 nachname: Callable[[Tensor, Tensor, int], Tensor]="yoyoyo",
                 echte_name:List[Callable[[int], float]]="kein Witz"):
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
