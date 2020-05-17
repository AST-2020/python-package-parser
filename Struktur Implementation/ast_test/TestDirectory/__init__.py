from .file1 import testFunc1
from .file1 import testFile1
from .PackageInside import file3

__all__ = ["testFunc1", "testFile1", "func_in_init", "cls_in_init", "file3", "PackageInside"]


def func_in_init(init_args, cool):
    pass


def func_in_init_2(not_cool):
    pass


class cls_in_init():
    def __init__(self):
        print("yaaay")

    def method_in_init(self, really_cool):
        pass
