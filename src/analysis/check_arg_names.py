from typing import List

from analysis._utils import get_parameters, function_not_found_error, qualified_name
from analysis.message import MessageManager, Message
from library.model import Package
from user_code.model import Location


def check_arg_names(package: Package, location: Location, module_path: str, keyword_arguments: List[str],
                    func_name: str, receiver_class_name: str = None):
    message_manager = MessageManager()

    parameters = get_parameters(package, module_path, func_name, receiver_class_name)
    if parameters is None:
        message_manager.add_message(function_not_found_error(func_name, location))
        message_manager.print_messages()
        return
    param_names = [parameter.get_name() for parameter in parameters]

    # Actual comparison
    for key in keyword_arguments:
        if key not in param_names:
            new_error = _unknown_parameter_error(location, module_path, func_name, key)
            message_manager.add_message(new_error)

    message_manager.print_messages()


def _unknown_parameter_error(location: Location, module_path: str, func_name: str, argument_name: str):
    return Message(location, f"{qualified_name(module_path, func_name)} has no parameter named '{argument_name}'.")
