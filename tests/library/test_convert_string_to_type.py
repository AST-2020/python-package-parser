from unittest import TestCase
from src.library.convert_string_to_type import convert_string_to_type


class Test_Convert_String_To_Obj(TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_Convert_String_To_Obj, self).__init__(*args, **kwargs)

    def test_method_with_parameter_ex1(self):
        self.assertEqual("<class 'int'>", str(convert_string_to_type("int")))

    def test_method_with_parameter_ex2(self):
        self.assertEqual("<class 'dict'>", str(convert_string_to_type("dict")))

    def test_method_with_parameter_ex3(self):
        self.assertEqual("<class 'list'>", str(convert_string_to_type("list")))

    def test_method_with_parameter_ex4(self):
        self.assertEqual("<class 'float'>", str(convert_string_to_type("float")))

    def test_method_with_parameter_ex5(self):
        self.assertEqual("<class 'tuple'>",  str(convert_string_to_type("tuple")))

    def test_method_with_parameter_ex6(self):
        self.assertEqual("None", str(convert_string_to_type("None")))

    def test_method_with_parameter_ex7(self):
        self.assertEqual("typing.Iterable[int]", str(convert_string_to_type("Iterable[int]")))

    def test_method_with_parameter_ex8(self):
        self.assertEqual("typing.Callable[[str], NoneType]", str(convert_string_to_type("Callable[[str], None]")))

    # List have to be written with capital "L"
    def test_method_with_parameter_ex9(self):
        self.assertEqual("typing.List[NoneType]", str(convert_string_to_type("List[None]")))

    def test_method_with_parameter_ex10(self):
        self.assertEqual("typing.List[int]", str(convert_string_to_type("List[int]")))

    def test_method_with_parameter_ex11(self):
        self.assertEqual("typing.Union[int, typing.Any]", str(convert_string_to_type("Union[int, device]")))

    def test_method_with_parameter_ex12(self):
        self.assertEqual("typing.Union[int, str]", str(convert_string_to_type("union[int,str]")))

    def test_method_with_parameter_ex13(self):
        self.assertEqual("typing.Union[typing.Any, str, int, NoneType]",
                         str(convert_string_to_type("Optional[Union[_device, str, int]]")))

    def test_method_with_parameter_ex14(self):
        self.assertEqual("typing.Callable[..., str]",
                         str(convert_string_to_type("Callable[..., str]")))

    def test_method_with_parameter_ex15(self):
        self.assertEqual("typing.Tuple[typing.List[typing.Callable[[int], float]], typing.Any]",
                         str(convert_string_to_type("Tuple[List[Callable[[int], float]], device]")))

    def test_method_with_parameter_ex16(self):
        self.assertEqual("typing.Callable[[typing.Any, typing.Any, typing.Any], typing.Any]",
                         str(convert_string_to_type("Callable[[Module, _grad_t, _grad_t], Tensor]]")))

    def test_method_with_parameter_ex17(self):
        self.assertEqual("typing.Callable[[torch.Tensor, torch.Tensor, int], torch.Tensor]",
                         str(convert_string_to_type("Callable[[Tensor, Tensor, int], Tensor]")))

    def test_method_with_parameter_ex18(self):
        self.assertEqual("typing.Tuple[torch.Tensor, ...]", str(convert_string_to_type("Tuple[Tensor, ...]")))

    def test_method_with_parameter_ex19(self):
        self.assertEqual("['donde', 'esta', 'la', 'biblioteca', 3.14]",
                         str(convert_string_to_type("['donde', 'esta', 'la', 'biblioteca', 3.14]")))

