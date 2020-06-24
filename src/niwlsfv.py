import re
from torch import Tensor
from src.library.model._parameter import Parameter
from src.library.model._function import Function
from src.library.model._klass import Class
from typing import *

print(eval("type(None)"))



# parameters = []
# expected_results = []
# parameters.append(Parameter("arg1"))
# parameters.append(Parameter("arg3", eval("int")))
# parameters.append(Parameter("arg4", None))
# parameters.append(Parameter("arg6", has_default=True, default=2.4))
# parameters.append(Parameter("arg7", has_default=False, default=None))
# parameters.append(Parameter("arg8", eval("float"), True, 2))
#
# function = Function("empty", parameters)
#
# function1 = Function("function1", [Parameter("arg1"),
#                           Parameter("arg2", eval("int")),
#                           Parameter("arg3", None),
#                           Parameter("arg4", has_default=True, default=2.4)])
# function2 = Function("function1", [Parameter("arg2")])
#
# function3 = Function("empty_func", None)
#
# # class instanes to test
# klasses = []
#
# klasses.append(Class("klass0"))
# klasses.append(Class("klass1"))
# klasses[1].add_method(function1)
# klasses.append(Class("klass2"))
# klasses[2].add_method(function1)
# klasses[2].add_method(function2)
# klasses.append(Class("klass3", [function1]))
# klasses.append(Class("klass4", [function1, function2]))
# klasses.append(Class("klass5"))
# klasses[5].add_method(function3)
# klasses.append(Class("klass6"))
# klasses[6].add_method(function1)
# klasses[6].add_method(function3)

# expected
expected_result_for_methods_with_same_name = {"klass1": {}, "klass2": {}, "klass3": {}, "klass4": {},
   "klass5": {}, "klass6": {}}

expected_result_for_methods_with_same_name["klass2"]["function1"] = \
    ["def function1(arg1, arg2, arg3, arg4)", "def function1(arg2)"]

expected_result_for_methods_with_same_name["klass3"]["function1"] = ["def function1(arg1, arg2, arg3, arg4)"]
#
# expected_result_for_methods_with_same_name["klass4"]["function1"] = \
#     ["def function1(arg1, arg2, arg3, arg4)", "def function1(arg2)"]
#
# expected_result_for_methods_with_same_name["klass5"]["empty_func"] = ["def empty_func(None)"]
# expected_result_for_methods_with_same_name["klass6"]["empty_func"] = ["def empty_func(None)"]
# expected_result_for_methods_with_same_name["klass6"]["function1"] = ["def function1(arg1, arg2, arg3, arg4)"]

# for i in range(len(klasses)):
#     if len(klasses[i].get_all_methods()) == 0:
#         pass
#     else:
#         method_lists = klasses[i].get_all_methods()
#
#         for methods_with_same_name in method_lists:
#             for j in range(len(methods_with_same_name)):
#                 method_name = methods_with_same_name[0].get_name()
#                 expected_result_for_methods_with_same_name["klass" + str(i + 1)][method_name]
#
#                 # print(methods_with_same_name[j].__str__() in expected_result_for_methods_with_same_name["klass" + str(i+1)][method_name])
#                 # print(len(methods_with_same_name) == len(expected_result_for_methods_with_same_name["klass" + str(i+1)][method_name]))