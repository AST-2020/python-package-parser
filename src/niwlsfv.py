import re
xx = "Callable[[Tensor, Tensor, int], int]"
result = re.match("^Callable\\[\\[(.*)]$", xx)
result = result.group(1).rsplit("], ")
print(result[0])
print(result[1])
print(type(None))
