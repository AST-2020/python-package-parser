from src.library.parser import parse_package, parse_packages
from src.library.parser import parse_package
from src.library import parser
from src.library.parser import parse_package


if __name__ == '__main__':
    modules_names =[]
    module_functions = {}
    module_classes_names_and_methods = {}
    # package = parse_package("TestPackage_3")
    # all_modules = package.get_all_modules()
    # for module in all_modules:
    #     module_name = module.get_name()
    #     modules_names.append(module_name)
    #     module_classes = module.get_all_classes()
    #     for klass in module_classes:
    #         klass_methods = klass.get_all_methods()
    #         for method in klass_methods:
    #             method_parameters = method.get_parameters()
    #             for parameter in method_parameters:
    #                 if parameter.get_name() == "file2_init":
    #                     print(True)





    # print(modules_names)
    # parsed_package = _walk_package("TestPackage")
    # for module_path, python_file, python_interface_file in parsed_package:
    #     print(module_path, " ", python_file, " ", python_interface_file)
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
    # methods = package.get_top_level_functions_with_name("TestDirectory.file1", "testFunc1")
    # for method in methods:
    #     print(method)
    #     parameters = method.get_parameters()
    #     for parameter in parameters:
    #         print(parameter)
    #     print("############")

    # methods = package.get_methods_with_name("TestPackage_3.UC4_pyi_files", "testFile5", "method_52")
    # for method in methods:
    #     print(method)
    #     parameters = method.get_parameters()
    #     for parameter in parameters:
    #         print(parameter)
    #     print("############")

    # methods = package.get_top_level_functions_with_name("TestDirectory.file1", "empty_func")
    # for method in methods:
    #     print(method)
    #     parameters = method.get_parameters()
    #     for parameter in parameters:
    #         print(parameter)
    #     print("############")

    # methods = package.get_methods_with_name("TestDirectory.file1", "empty_cls", "empty_method")
    # for method in methods:
    #     print(method)
    #     parameters = method.get_parameters()
    #     for parameter in parameters:
    #         print(parameter)
    #     print("############")
    result_package = parse_package("tests.library.TestDirectory.TestPackage_2")
    # methods_with_same_name = result_package.get_methods_with_name(
    #     "tests.library.TestDirectory.TestPackage_2.UC2_and_3", "test_class2", "test_func_2")
    # for method in methods_with_same_name:
    #     print(method)

    methods_with_same_name = result_package.get_top_level_functions_with_name(
        "tests.library.TestDirectory.TestPackage_2.UC4_pyi_files", "testFunc52")
    for method in methods_with_same_name:
        print(method)
        for parameter in method.get_parameters():
            print(parameter.__str__())
        print("###########")
