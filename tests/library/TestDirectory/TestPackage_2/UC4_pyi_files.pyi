from typing import List, Dict, overload, Tuple, Callable, Optional, Union, Any
from torch import Tensor

from library.model import Module

class testFile5:
    def __init__(self, name: Optional[Union[_device, str, int]], nachname:Optional[int],
                 echte_name:Callable[[Tensor, Tensor, int], Tensor]):
        pass
    def method_51(self, name: Dict[float, _device], nachname:Callable[[Tensor, Tensor, int], Tensor],
                 echte_name):
        pass
    def method_52(self, name: Union[..., Tensor], nachname:Callable[[Tensor, Tensor, int], Tensor],
                 echte_name:Callable[['Module'], None]):
        pass
    def method_53(self,
                 name:Union[Callable[[int], float], List[Callable[[int], float]]],
                 nachname: Callable[[Tensor, Tensor, int], Tensor]="yoyoyo",
                 echte_name:List[Callable[[int], float]]="kein Witz"):
        pass


obj = testFile5()

def testFunc51(num:str, my_list:List, my_bool:bool=..., my_double:float=..., my_obj:obj=...) -> int:
    pass

@overload
def testFunc51(num:str, my_list:Dict, my_bool:bool, my_double:Double, my_obj:obj=...) -> int:
    pass


def testFunc52(arg0:Dict, arg1:str, arg2:Tuple[List[Callable[[int], float]], str, float, obj]):
    pass
