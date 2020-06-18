from src.library import parser
from src.library.parser import parse_package
from tests.library import TestDirectory

if __name__ == '__main__':
    package = parse_package("tests.library_tests.TestDirectory")
    for module in package.get_all_modules():
        print(module.get_name())

        print("  Classes\n  =======")
        for klass in module.get_all_classes():
            print(f"    {klass}")

        print("  Functions\n  =========")
        for function in module.get_all_top_level_functions():
            print(f"    {function}")
