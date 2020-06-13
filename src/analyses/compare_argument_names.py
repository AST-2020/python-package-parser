from typing import List

from analyses._utils import get_parameters
from analyses.messages import MessageManager, Message
from library.model import Package


def compare_arg_names(package: Package, file: str, line: int, import_path: str, keyword_arguments: List[str],
                      func_name: str, receiver_class_name: str = None):
    message_manager = MessageManager()

    parameters = get_parameters(package, import_path, func_name, receiver_class_name)
    if parameters is None:
        function_not_found_error = Message("", line,
                                           "The function [" + func_name + "] or the path [" + import_path + "] does not exist.",
                                           file)
        message_manager.add_message(function_not_found_error)
        message_manager.print_messages()
        return 1

    param_names = [parameter.get_name() for parameter in parameters]

    for key in keyword_arguments:
        if key not in param_names:
            new_error = Message(import_path + "." + func_name, line, "Parameter [" + key + "] not found.", file)
            message_manager.add_message(new_error)

    message_manager.print_messages()