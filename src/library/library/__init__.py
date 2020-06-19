from library.parser import parse_package
import TestDirectory

if __name__ == '__main__':
    package = parse_package("TestDirectory")
    # for module in package.get_all_modules():
    #     print(module.get_name())
    #
    #     print("  Classes\n  =======")
    #     for klass in module.get_all_classes():
    #         print(f"    {klass}")
    #
    #     print("  Functions\n  =========")
    #     for function in module.get_all_top_level_functions():
    #         print(f"    {function}")
    methods = package.get_top_level_functions_with_name("TestDirectory.file1", "testFunc1")
    for method in methods:
        print(method)
        parameters = method.get_parameters()
        for parameter in parameters:
            print(parameter)
        print("############")



    methods = package.get_methods_with_name("TestDirectory.file1", "testFile2", "__init__")
    for method in methods:
        print(method)
        parameters = method.get_parameters()
        for parameter in parameters:
            print(parameter)
        print("############")

    methods = package.get_top_level_functions_with_name("TestDirectory.file1", "empty_func")
    for method in methods:
        print(method)
        parameters = method.get_parameters()
        for parameter in parameters:
            print(parameter)
        print("############")
