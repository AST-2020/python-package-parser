from analysis._utils import get_parameters, function_not_found_error, qualified_name
from analysis.message import MessageManager, Message
from library.model import Package
from user_code.model import FunctionCall


def check_arg_names(message_manager: MessageManager, call: FunctionCall, package: Package, module_path: str,
                    func_name: str, receiver_class_name: str = None):
    parameters = get_parameters(package, module_path, func_name, receiver_class_name)
    if parameters is None:
        message_manager.add_message(function_not_found_error(func_name, call.location))
        return
    param_names = [parameter.get_name() for parameter in parameters]

    # Actual comparison
    for key in call.keyword_arg_names:
        if key not in param_names:
            new_error = _unknown_parameter_error(call, module_path, func_name, key)
            message_manager.add_message(new_error)


def _unknown_parameter_error(call: FunctionCall, module_path: str, func_name: str, argument_name: str):
    return Message(call.location, f"Function '{qualified_name(module_path, func_name)}' has no parameter named '{argument_name}'.")
