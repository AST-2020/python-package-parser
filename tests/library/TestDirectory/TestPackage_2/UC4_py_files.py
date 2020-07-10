from typing import *
from torch import Tensor


class testFile4:
    def __init__(self, my_int: int, my_dict: Dict, my_bool: bool = "True", my_float: float = 2.5):
        pass

    def method_for_testFile4(self, my_union: Union[int, bool], my_optional: Optional[int],
                             my_callable: Callable[[Tensor], None]):
        pass


def testFunc4(param_0: Optional[Union[_device, str, int]], param_1: Optional[int],
                 param_2: Callable[[Tensor, Tensor, int], Tensor], param_3: Callable[..., Tensor]):
    pass


def testFunc41(param_0: Dict[float, _device], param_1: Callable[[Tensor, Tensor, int], Tensor],
                 param_2):
    pass
