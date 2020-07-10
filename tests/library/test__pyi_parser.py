from unittest import TestCase
import ast
from src.library.model._module import Module
from src.library.model._klass import Class
from src.library.model._function import Function
from src.library.model._parameter import Parameter
from src.library.parser._pyi_parser import _PythonPyiFileVisitor


# def __init__(self, function_name, searched_args: OrderedDict, searched_cls_name=None):


class Test_PythonPyiFileVisitor(TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_PythonPyiFileVisitor, self).__init__(*args, **kwargs)

    with open("tests/library/TestDirectory/TestPackage/file1.pyi", mode="r", encoding='utf-8') as f:
        contents = f.read()
        tree = ast.parse(contents)

    def find_func_type_hints(self):
        # def __init__(self, module, function_name, searched_args: OrderedDict, searched_cls_name=None):
        func_name = "foo1"
        searched_args = {"param1":None, "param2":None, "param3":None}
        actual_type_hints = _PythonPyiFileVisitor(func_name, searched_args)

