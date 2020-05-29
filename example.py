from torch.onnx.symbolic_opset9 import randn
from torch.tensor import Tensor
from torch.nn.modules import linear as lin
import torch

dtype: torch.dtype = torch.float

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10

# funktion
x: Tensor = randn(N, D_in, dype=dtype)                      # should give an error
w1: Tensor = randn(N, D_out, dtype=dtype)

# constructor
l1: lin.Linear = lin.Linear(in_fetures=D_in, out_features=H) # should give an error
l2: lin.Linear = lin.Linear(in_features=D_in, out_features=H)

# methode
x.norm(dtpe=dtype)                                            # should give an error
x.norm(dtype=dtype)