import torch as t
import numpy as np


dtype = t.float
dev = t.device("cpu")
# device = torch.device("cuda:0") # Uncomment this to run on GPU

# N is batch size; D_in is input dimension;
# H is hidden dimension; D_out is output dimension.
N, D_in, H, D_out = 64, 1000, 100, 10

# Create random input and output data
x = t.randn(N, D_in, device=dev, dtype=dtype)
y = t.randn(N, D_out, device=dev, dtype=dtype)