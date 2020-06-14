from analysis.message import MessageManager, Message
from user_code.model import FunctionCall


def check_function_exists(call: FunctionCall, message_manager: MessageManager):
    if not call.callee_candidates:
        message_manager.add_message(function_not_found_error(call))


def function_not_found_error(call: FunctionCall) -> Message:
    return Message(call.location, f"Function '{call.name}' was not found.")
