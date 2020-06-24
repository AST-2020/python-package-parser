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
    # param = [] # soll gelöscht werden
    # for key in call.positional_args:
    #     pass
    #
    # for key in call.keyword_arg:
    #     pass
    name = call.name
    args = call.positional_arg
    keyargs= call.keyword_arg

    package_info = call.callee_candidates

    # for p in package_info:
    #     print(str(p.get_name()), str(p.get_parameters()))
    #     for name in p.get_parameters():
    #         print(str(name.get_name()),': ' ,name.get_type_hint(), name.get_default())
    print(name)
    for arg in args:
        print( arg.value ,': ', arg.type)
    for kwarg in keyargs:
        print(kwarg.name,': ',kwarg.value, ': ', kwarg.type)