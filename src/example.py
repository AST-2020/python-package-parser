from torch.onnx.symbolic_opset9 import randn
from torch.tensor import Tensor
from torch.cuda import current_device #--
import torch

dtype: torch.dtype = torch.float
device: torch.device = torch.device('cpu')

# current_device(20.3 , 'str' ,[1,3,4] ,{'a':1} ,a= True, b = 4)

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10
N = 5
# funktion
x1: Tensor = randn(34, N,  D_in, dtype= 5, device=D_out)       # should give an error
x2: Tensor = randn()                                          # should give an error
x3: Tensor = randn(N, D_in, dtype=dtype)
N = 10