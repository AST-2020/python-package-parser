from torch.onnx.symbolic_opset9 import randn
from torch.tensor import Tensor
from torch.cuda import current_device #--
import torch
from torch.nn.functional import fractional_max_pool3d_with_indices,  max_pool2d_with_indices
class Ob():
    pass

obj1 = Ob()
obj2 = Ob()

oblist = [obj1, obj2]


dtype: torch.dtype = torch.float
device: torch.device = torch.device('cpu')
obj =torch.Tensor()

d = {'a':3}

# current_device(20.3 , 'str' ,[1,3,4] ,{'a':1} ,a= True, b = 4)

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10
N = 5
# funktion
# fractional_max_pool3d_with_indices(g = oblist, input=obj, kernel_size="kernel_size", output_size="output_size=None",
#                                        output_ratio=None, return_indices=False, _random_samples=None)

max_pool2d_with_indices('input', 'kernel_size', 'None', padding=5, dilation='str',
                        ceil_mode=True, return_indices=5.2)
# x1: Tensor = randn(34, N,  D_in, dtype= 5, device=D_out)       # should give an error
# x2: Tensor = randn()                                          # should give an error
# x3: Tensor = randn(N, D_in, dtype=dtype)
