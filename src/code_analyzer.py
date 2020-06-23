import sys
from typing import List

import torch

from analysis import check_function_exists, check_arg_names, check_arg_number
from analysis.message import MessageManager
from library.model import Package
from library.parser import parse_packages, parse_package
from user_code.parser import parse_function_calls


def analyze_files(files_to_analyze: List[str], package: Package,
                  message_manager: MessageManager = None) -> MessageManager:
    if message_manager is None:
        message_manager = MessageManager()

    for file_to_analyze in files_to_analyze:
        analyze_file(file_to_analyze, package, message_manager)

    return message_manager


def analyze_file(file_to_analyze: str, package: Package, message_manager: MessageManager = None) -> MessageManager:
    if message_manager is None:
        message_manager = MessageManager()

    calls = parse_function_calls(file_to_analyze, package)

    for call in calls:
        check_function_exists(call, message_manager)
        check_arg_names(call, message_manager)
        check_arg_number(call, message_manager)

    return message_manager


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        package = parse_packages(["torch", "sklearn"])
    #     # for module in package.get_all_modules():
    #     #     print(module.get_name())
    #     #
    #     #     print("  Classes\n  =======")
    #     #     for klass in module.get_all_classes():
    #     #         print(f"    {klass}")
    #     #
    #     #     print("  Functions\n  =========")
    #     #     for function in module.get_all_top_level_functions():
    #     #         print(f"    {function}")
    #     methods = package.get_methods_with_name("torch.utils.data.sampler", "BatchSampler", "__init__")
    #     for method in methods:
    #         parameters = method.get_parameters()
    #         for parameter in parameters:
    #             print(parameter)

        # analyze_files(sys.argv[1:], parse_packages(['torch', 'sklearn'])).print_messages()
    else:
        print('Usage: python code_analyzer.py <files_to_analyze*>')
