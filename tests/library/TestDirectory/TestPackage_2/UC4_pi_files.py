from typing import *
from torch import Tensor


class testFile4:
    def __init__(self, my_int: int, my_dict: Dict, my_bool: bool = "True", my_float: float = 2.5):
        pass

    def method_for_testFile4(self, my_union: Union[int, bool], my_optional: Optional[int],
                             my_callable: Callable[[Tensor], None]):
        pass


def testFunc4(name: Optional[Union[_device, str, int]], nachname:Optional[int],
                 echte_name:Callable[[Tensor, Tensor, int], Tensor]):
    pass


def testFunc41(name: Dict[float, _device], nachname:Callable[[Tensor, Tensor, int], Tensor],
                 echte_name):
    pass




