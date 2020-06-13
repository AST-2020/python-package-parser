from typing import List

from analyses._utils import get_parameters
from analyses.messages import MessageManager, Message
from library.model import Package


def compare_arg_amount(package: Package, file: str, line: int, import_path: str, keyword_arguments: List[str],
                       arg_values: List, func_name: str, receiver_class_name: str):
    message_manager = MessageManager()

    # user_total_args: arguments given by the user
    user_total_args = len(keyword_arguments) + len(arg_values)  # Save total number of arguments given by the user

    # This case is for when class name is not present
    # That means we are working with a function, so the program calls related methods from Hady's code.
    func_or_method_args = get_parameters(package, import_path, func_name, receiver_class_name)

    if func_or_method_args is None:
        new_error = Message(import_path + "." + func_name, line, "Function/method " + func_name + " not found.",
                            file)
        message_manager.add_message(new_error)
        message_manager.print_messages()
        return

    maximum, minimum = get_expected_number_of_arguments(func_or_method_args)

    if not minimum <= user_total_args <= maximum:
        new_error = Message(import_path + "." + func_name, line,
                            "Wrong number of parameters (" + str(user_total_args) + "). Max: " + str(maximum)
                            + " Min: " + str(minimum), file)
        message_manager.add_message(new_error)

    message_manager.print_messages()


def get_expected_number_of_arguments(func_or_method_args):
    maximum = len(func_or_method_args)
    minimum = 0

    # Total number of parameters
    for p in func_or_method_args:
        if not p.has_default():
            minimum += 1  # For every parameter that does NOT have a default value, minimum increased by 1

    return maximum, minimum