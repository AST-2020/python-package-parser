from typing import List

from analysis._utils import get_parameters
from analysis.message import MessageManager, Message
from library.model import Parameter
from user_code.model import FunctionCall


def check_arg_number(call: FunctionCall, message_manager: MessageManager):
    parameters = get_parameters(call.callee_candidates)
    if parameters is None:
        return

    # Actual comparison
    given_args = _given_number_of_arguments(call)
    min_expected_args, max_expected_args = _expected_number_of_arguments(parameters)
    if not min_expected_args <= given_args <= max_expected_args:
        message_manager.add_message(
            _wrong_number_of_arguments_error(call, min_expected_args, max_expected_args, given_args)
        )


def _given_number_of_arguments(call: FunctionCall):
    return call.number_of_positional_args + len(call.keyword_arg_names)


def _expected_number_of_arguments(parameters: List[Parameter]) -> (int, int):
    minimum = 0
    maximum = len(parameters)

    for p in parameters:
        if not p.has_default():
            minimum += 1

    return minimum, maximum


def _wrong_number_of_arguments_error(call: FunctionCall, min_expected_args: int, max_expected_args: int,
                                     given_args: int):
    if min_expected_args == max_expected_args:
        expected = f"exactly {min_expected_args}"
    else:
        expected = f"between {min_expected_args} and {max_expected_args}"

    return Message(
        call.location,
        f"Function '{call.name}' expects {expected} arguments but got {given_args}."
    )
