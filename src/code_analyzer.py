import sys

from analysis import check_function_exists, check_arg_names, check_arg_number
from analysis.message import MessageManager
from library.model import Package
from library.parser import parse_package
from user_code.parser._function_parser import parse_function_calls


def parse_code(file_to_analyze: str, package: Package):
    """
    This function combines all of the python files to first visit the user code 'file' for imports, then variables, then
    functions and methods.
    """

    calls = parse_function_calls(file_to_analyze, package)

    message_manager = MessageManager()
    for call in calls:
        check_function_exists(call, message_manager)
        check_arg_names(call, message_manager)
        check_arg_number(call, message_manager)
    message_manager.print_messages()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]

        # parse torch and sklearn library
        torch = parse_package('torch')
        sklearn = parse_package('sklearn')

        # parse code for both libraries
        parse_code(file_path, torch)
        # parse_code(file_path, sklearn)

        # TODO do not show torch errors when checking sklearn

    else:
        print('Usage: python code_analyzer.py <file_to_analyze>')
