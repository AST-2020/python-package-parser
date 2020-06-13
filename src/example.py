from torch.onnx.symbolic_opset9 import randn
from torch.tensor import Tensor
import torch

dtype: torch.dtype = torch.float
device: torch.device = torch.device('cpu')

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10

# funktion
x1: Tensor = randn(N, D_in, dtype=dtype, device=device)       # should give an error
x2: Tensor = randn()                                          # should give an error
x3: Tensor = randn(N, D_in, dtype=dtype)
