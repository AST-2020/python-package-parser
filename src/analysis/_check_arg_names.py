from analysis._utils import get_parameters
from analysis.message import MessageManager, Message
from user_code.model import FunctionCall


def check_arg_names(call: FunctionCall, message_manager: MessageManager):
    parameters = get_parameters(call.callee_candidates)
    if parameters is None:
        return

    param_names = [parameter.get_name() for parameter in parameters]

    # Actual comparison
    for key in call.keyword_arg_names:
        if key not in param_names:
            message_manager.add_message(_unknown_parameter_error(call, key))


def _unknown_parameter_error(call: FunctionCall, argument_name: str):
    return Message(
        call.location,
        f"Function '{call.name}' has no parameter named '{argument_name}'."
    )
