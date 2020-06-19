from analysis._utils import get_parameters
from analysis.message import MessageManager, Message
from user_code.model import FunctionCall

def check_type(call: FunctionCall, message_manager: MessageManager):
    parameters = get_parameters(call.callee_candidates)
    if parameters is None:
        return
    # param =  hier sollen wir eine List von tupel von name & type e.g. [(a,int), (b,Str) .....]
    #                                                                    [('s', str), ....]
    # arg = [(value, type), (value, type), .....]
    #             arg1            arg2
    # kw_arg[(name, value, type),.....]

    # f(4, c = 5)
    param = [] # soll gelöscht werden
    for key in call.positional_args:
        pass

    for key in call.keyword_arg:
        pass
