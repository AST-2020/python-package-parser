from analysis._utils import get_parameters
from analysis.message import MessageManager, Message
from user_code.model import FunctionCall
from typing import Any


# self.keyword_arg: List[Kw_arg] = keyword_arg  # -- User mit arg_name
# self.positional_arg: List[Arg] = positional_arg  # -- User ohne arg_name
# Callee Candidate List[methoden oder Funktionen] wenn : len > 1 --> break


def check_type(call: FunctionCall, message_manager: MessageManager):
    parameters = get_parameters(call.callee_candidates)
    if parameters is None:
        return

    args = call.positional_arg
    kw_args = call.keyword_arg

    function_or_method = call.callee_candidates[0]
    structure_args = [(par.get_name(), par.get_type_hint()) for par in function_or_method.get_parameters()]
    # print(structure_args)

    # primitiv_type = [eval("int"), eval("str"), eval("float"), eval("bool"), eval("Any"), eval("dict")]
    primitiv_type = [int, str, float, bool, Any, dict]
    index = 0
    # print(structure_args[0])
    for arg in args:
        # print(structure_args[index][0],' ' , structure_args[index][1], '  ',arg.get_value(), arg.get_type())
        if structure_args[index][1] in primitiv_type:
            # print(structure_args[index][1],'  ' ,arg.get_type())
            if arg.get_type() != structure_args[index][1] and structure_args[index][1] is not Any:
                # print('hier sollt eine fffff')
                message_manager.add_message(_unknown_parameter_error(call,structure_args[index][0], arg.get_type(), structure_args[index][1]))
            index = index + 1
        else:
            index = index+1
            continue

    for kw in kw_args:
        # print(kw.value, kw.type)
        for pa in structure_args:
            # print(pa[0], " ", pa[1], " ", kw.name," ", kw.type)
            if pa[1] in primitiv_type and pa[0] == kw.name:
                # print(pa[0],'  ', pa[1],'  ' ,arg.get_type())
                if kw.get_type() != pa[1] and pa[1] is not Any:
                    pass
                    # print('hier sollt eine fffff')
                    message_manager.add_message(_unknown_parameter_error(call, pa[0], kw.get_type(), pa[1]))
            else:
                continue

    # for arg in args:
    #     if isinstance(structure_args[index],list):
    #         print('liste')
    #         for l in structure_args[index][1]:
    #             index = index + 1
    #             if l is not Any:
    #                 print(l, arg.get_type())
    #                 if arg.get_type() != l:
    #                     print('pos : hier ist einen Fehler')
    #
    #     else:
    #         print('----------', structure_args[index][1])
    #         if structure_args[index][1] is not Any:
    #             if arg.get_type() != structure_args[index][1]:
    #                 print(arg.get_type(), structure_args[index][1], structure_args[0])
    #                 index = index + 1
    #                 print('pos : hier ist einen Fehler')
    #
    # for kw in kw_args:
    #     for pa in structure_args:
    #         if kw.name == pa[0]:
    #             if isinstance(pa[1], list):
    #                 for l in pa[1]:
    #                     if l is not Any:
    #                         if kw.get_type() != l:
    #                             print('kw : hier ist einen Fehler')
    #             else:
    #                 if pa[1] is not Any:
    #                     if kw.get_type() != pa[1]:
    #                         print('kw : hier ist einen Fehler')
    #



    # typhints = [(par.get_name(), par.get_type_hint()) for par in function_or_method.get_parameters()]
    # for p in typhints:
    #     if (p, Union):
    #     print(p[0],p[1])

    # name = call.name
    # args = call.positional_arg
    # keyargs= call.keyword_arg
    #
    # print(name)
    # for arg in args:
    #     print(arg.value, ': ', arg.type)
    # for kwarg in keyargs:
    #     print(kwarg.name, ': ', kwarg.value, ': ', kwarg.type)
def _unknown_parameter_error(call: FunctionCall, argument_name: str, given: str ,exp: str):
    return Message(
        call.location,
        f"Function '{call.name}' the type of  '{argument_name}' is not correct. expected: '{exp.__name__}', given: '{given.__name__}'"
    )