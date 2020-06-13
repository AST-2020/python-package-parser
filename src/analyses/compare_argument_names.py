from typing import List

from analyses._utils import get_parameters, function_not_found_error, qualified_name
from analyses.messages import MessageManager, Message
from library.model import Package


def compare_arg_names(package: Package, file: str, line: int, import_path: str, keyword_arguments: List[str],
                      func_name: str, receiver_class_name: str = None):
    message_manager = MessageManager()

    parameters = get_parameters(package, import_path, func_name, receiver_class_name)
    if parameters is None:
        message_manager.add_message(function_not_found_error(func_name, file, line))
        message_manager.print_messages()
        return
    param_names = [parameter.get_name() for parameter in parameters]

    # Actual comparison
    for key in keyword_arguments:
        if key not in param_names:
            new_error = _unknown_parameter_error(file, line, func_name, import_path, key)
            message_manager.add_message(new_error)

    message_manager.print_messages()


def _unknown_parameter_error(file: str, line: int, func_name: str, import_path: str, argument_name: str):
    return Message(file, line, f"{qualified_name(import_path, func_name)} has no parameter named '{argument_name}'.")
