from unittest import TestCase


class Test(TestCase):

    # plan:
    # 1- test primitive types
    # 2- test Callable[[],] and  Callable[...,]
    # 3- test Union[], Optional[] and Tensor
    # 4- test type hints that include ...
    # 5- test type hints that has None
    # 6- test type hints that has type_hints that has types that we don't support
    # 7- List


    # Examples from package:
    # Callable[[Module, _grad_t, _grad_t], Union[type(None), Tensor]]
    # Callable[['Module'], None]
    # Union[Callable[[int], float]
    # List[Callable[[int], float]]]
    # int
    # float
    # dict
    # Tuple
    # Iterable[int]
    # bool
    # Optional[int]
    # Any
    # Callable[[Tensor, Tensor, int], Tensor]
    # Union[int, device]
    # Optional[Union[_device, str]]
    # Tuple[Tensor, ...]

    def test_convert_string_to_type(self):
        self.fail()
