from torch.onnx.symbolic_opset9 import randn
from torch.tensor import Tensor
from torch.cuda import current_device #--
from torch.testing._internal.distributed.rpc.jit.rpc_test import assorted_types_args_kwargs
from torch.nn.functional import fractional_max_pool3d_with_indices,  max_pool2d_with_indices
from torch.functional import split, lu_unpack
from torch.autograd.grad_mode  import  set_grad_enabled # für pyi_datei

# Example for pyi file
# mode = bool, but here int is given.
set_grad_enabled(mode = 1)

# Create a tensor object to use later.
t = Tensor()

# This example is for py file.
# assorted_types_args_kwargs(tensor_arg: Tensor, str_arg: str, int_arg: int, tensor_kwarg: Tensor = torch.tensor([2, 2]),str_kwarg: str = "str_kwarg",
# int_kwarg: int = 2,)
# Should give errors in: str_arg, int_arg, int_kwarg
assorted_types_args_kwargs(t, str_arg =True, int_arg = 3.5 , tensor_kwarg = t ,str_kwarg = "str_kwarg",int_kwarg = '2')

# Examples for docstrings.
split(t, 3.3, dim = True)
lu_unpack(t, t, True, 'string')