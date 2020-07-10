from analysis._utils import get_parameters
from analysis.message import MessageManager, Message
from user_code.model import FunctionCall

def check_default_value(call: FunctionCall, message_manager: MessageManager):
    parameters = get_parameters(call.callee_candidates)
    if parameters is None:
        return
    args = call.positional_arg
    kw_args = call.keyword_arg

    function_or_method = call.callee_candidates[0]
    structure_args = [(par.get_name(), par.has_default(), par.get_default()) for par in function_or_method.get_parameters()]

    index = 0
    for arg in args:
        if structure_args[index][1] is False:
            index = index +1
            continue
        else:
            if arg.get_value() == structure_args[index][2]:
                # print('positional has the same default value')
                message_manager.add_message(_unknown_parameter_error(call, structure_args[index][0]))
                index = index + 1

    # print('postional is finished ')
    for kw in kw_args:
        for pa in structure_args:
            if kw.name == pa[0]:
                if kw.get_value() == pa[2]:
                    # print('kw : has the same default value')
                    message_manager.add_message(_unknown_parameter_error(call, kw.name))


    # for pa in structure_args:
    #     print(pa[0], pa[1], pa[2])

    # typhints = [(par.get_name(), par.get_type_hint()) for par in function_or_method.get_parameters()]
    # for p in typhints:
    #     print(p[0],p[1])

def _unknown_parameter_error(call: FunctionCall, argument_name: str):
    return Message(
        call.location,
        f" in function '{call.name}' the  value of the parameter '{argument_name}' is the same as default value."
    , iswarning = True)