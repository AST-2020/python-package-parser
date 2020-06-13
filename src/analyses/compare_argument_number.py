from typing import List

from analyses._utils import get_parameters, function_not_found_error, qualified_name
from analyses.messages import MessageManager, Message
from library.model import Package, Parameter


def compare_arg_amount(package: Package, file: str, line: int, import_path: str, keyword_arguments: List[str],
                       arg_values: List, func_name: str, receiver_class_name: str):
    message_manager = MessageManager()

    parameters = get_parameters(package, import_path, func_name, receiver_class_name)
    if parameters is None:
        message_manager.add_message(function_not_found_error(func_name, file, line))
        message_manager.print_messages()
        return

    # Actual comparison
    given_args = _given_number_of_arguments(arg_values, keyword_arguments)
    min_expected_args, max_expected_args = _expected_number_of_arguments(parameters)
    if not min_expected_args <= given_args <= max_expected_args:
        new_error = _wrong_number_of_arguments_error(file, line, import_path, func_name, min_expected_args,
                                                     max_expected_args, given_args)
        message_manager.add_message(new_error)

    message_manager.print_messages()


def _given_number_of_arguments(arg_values: List, keyword_arguments: List):
    return len(arg_values) + len(keyword_arguments)


def _expected_number_of_arguments(parameters: List[Parameter]) -> (int, int):
    minimum = 0
    maximum = len(parameters)

    for p in parameters:
        if not p.has_default():
            minimum += 1

    return minimum, maximum


def _wrong_number_of_arguments_error(file: str, line: int, import_path: str, func_name: str, min_expected_args: int,
                                     max_expected_args: int, given_args: int):
    if min_expected_args == max_expected_args:
        expected = f"exactly {min_expected_args}"
    else:
        expected = f"between {min_expected_args} and {max_expected_args}"

    return Message(
        file,
        line,
        f"{qualified_name(import_path, func_name)} expects {expected} arguments but got {given_args}."
    )
