from typing import List

from analysis._utils import get_parameters, function_not_found_error, qualified_name
from analysis.message import MessageManager, Message
from library.model import Package, Parameter
from user_code.model import Location, FunctionCall


def check_arg_number(message_manager: MessageManager, call: FunctionCall, package: Package, module_path: str,
                     func_name: str, receiver_class_name: str):
    parameters = get_parameters(package, module_path, func_name, receiver_class_name)
    if parameters is None:
        message_manager.add_message(function_not_found_error(func_name, call.location))
        return

    # Actual comparison
    given_args = _given_number_of_arguments(call)
    min_expected_args, max_expected_args = _expected_number_of_arguments(parameters)
    if not min_expected_args <= given_args <= max_expected_args:
        new_error = _wrong_number_of_arguments_error(call.location, module_path, func_name, min_expected_args,
                                                     max_expected_args, given_args)
        message_manager.add_message(new_error)


def _given_number_of_arguments(call: FunctionCall):
    return call.number_of_positional_args + len(call.keyword_arg_names)


def _expected_number_of_arguments(parameters: List[Parameter]) -> (int, int):
    minimum = 0
    maximum = len(parameters)

    for p in parameters:
        if not p.has_default():
            minimum += 1

    return minimum, maximum


def _wrong_number_of_arguments_error(location: Location, module_path: str, func_name: str, min_expected_args: int,
                                     max_expected_args: int, given_args: int):
    if min_expected_args == max_expected_args:
        expected = f"exactly {min_expected_args}"
    else:
        expected = f"between {min_expected_args} and {max_expected_args}"

    return Message(
        location,
        f"Function '{qualified_name(module_path, func_name)}' expects {expected} arguments but got {given_args}."
    )
