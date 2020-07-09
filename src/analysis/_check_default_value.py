from analysis._utils import get_parameters
from analysis.message import MessageManager, Message
from user_code.model import FunctionCall

def check_default_value(call: FunctionCall, message_manager: MessageManager):
    pass
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
                index = index + 1
                print('positional has the same default value')

    # print('postional is finished ')
    for kw in kw_args:
        for pa in structure_args:
            if kw.name == pa[0]:
                if kw.get_value() == pa[2]:
                    print('kw : has the same default value')


    # for pa in structure_args:
    #     print(pa[0], pa[1], pa[2])





def _unknown_parameter_error(call: FunctionCall, argument_name: str):
    # return Message(
    #     call.location,
    #     f"Function '{call.name}' has no parameter named '{argument_name}'."
    # )
    pass