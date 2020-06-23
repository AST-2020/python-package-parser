import sys
from typing import List

from analysis import check_function_exists, check_arg_names, check_arg_number, check_type
from analysis.message import MessageManager
from library.model import Package
from library.parser import parse_packages
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
        # check_function_exists(call, message_manager)
        # check_arg_names(call, message_manager)
        # check_arg_number(call, message_manager)
        check_type(call, message_manager)
    return message_manager


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        analyze_files(sys.argv[1:], parse_packages(['torch', 'sklearn'])).print_messages()
    else:
        print('Usage: python code_analyzer.py <files_to_analyze*>')
