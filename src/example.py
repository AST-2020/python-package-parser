from torch.onnx.symbolic_opset9 import randn
from torch.tensor import Tensor
from torch.cuda import current_device #--
from torch.testing._internal.distributed.rpc.jit.rpc_test import assorted_types_args_kwargs

from torch.nn.functional import fractional_max_pool3d_with_indices,  max_pool2d_with_indices
from torch.functional import split, lu_unpack

from torch.autograd.grad_mode  import  set_grad_enabled # für pyi_datei

# set_grad_enabled(mode = 1 ) # für pyi_datei Hier sollte ein Fehler sein. node = bool
t = Tensor()
# assorted_types_args_kwargs(tensor_arg: Tensor, str_arg: str, int_arg: int, tensor_kwarg: Tensor = torch.tensor([2, 2]),str_kwarg: str = "str_kwarg",
# int_kwarg: int = 2,)
assorted_types_args_kwargs(t, str_arg =True, int_arg = 3.5 , tensor_kwarg = t ,str_kwarg = "str_kwarg",int_kwarg = '2') # für py_datei
# fehlrer für str_arg, int_arg, int_kwarg
split(t, 3.3, dim = True) # für docstring
lu_unpack(t, t, True, 'string')   # für doc string




# dtype: torch.dtype = torch.float
# device: torch.device = torch.device('cpu')
# obj =torch.Tensor()
#
# d = {'a':3}
#
# # current_device(20.3 , 'str' ,[1,3,4] ,{'a':1} ,a= True, b = 4)
#
# # N is batch size; D_in is input dimension;
# # H is hidden dimension; D_out is output dimension.
# N, D_in, H, D_out = 64, 1000, 100, 10
# N = 5
# # funktion
# fractional_max_pool3d_with_indices(1,2,3,4,return_indices = 5.5,b= 6)
#
# # max_pool2d_with_indices(None, padding=0, dilation=1,
# #                             ceil_mode=False)
# # x1: Tensor = randn(34, N,  D_in, dtype= 5, device=D_out)       # should give an error
# # x2: Tensor = randn()                                          # should give an error
# # x3: Tensor = randn(N, D_in, dtype=dtype)
