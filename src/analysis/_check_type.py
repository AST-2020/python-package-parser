from analysis._utils import get_parameters
from analysis.message import MessageManager, Message
from user_code.model import FunctionCall


def check_type(call: FunctionCall, message_manager: MessageManager):
    if len(call.callee_candidates) > 1 or len(call.callee_candidates) == 0:
        return
    # self.keyword_arg: List[Kw_arg] = keyword_arg  # -- User mit arg_name
    # self.positional_arg: List[Arg] = positional_arg  # -- User ohne arg_name
    # Callee Candidate List[methoden oder Funktionen] wenn :>1 break

    kw_args = [(kw_arg.name, kw_arg.type) for kw_arg in call.keyword_arg]
    positional_args = [pos_arg.type for pos_arg in call.positional_arg]
    structure_args = {}
    function_or_method = call.callee_candidates[0]

    for parameter in function_or_method.get_parameters():
        structure_args[parameter.get_name()] = parameter.get_type_hint()

    for i in range(len(kw_args)):
        if kw_args[i][0] in structure_args.keys():
            if structure_args.get(kw_args[i][0]) is not None and structure_args.get(kw_args[i][0]) == kw_args[i][1]:
                del structure_args[kw_args[i][0]]
            else:
                # it means that there is an error in type_hint
                print("error in type_hint")
        else:
            # it means that there is an error in arg_name
            print("error in arg_name or type_hint")
            # break is a possibility

    structure_args = [structure_args.values()]
    for i in range(min(len(positional_args), len(structure_args))):
        if structure_args[i] is not None and structure_args[i] != positional_args[i]:
            print("error in arg_name or type_hint")











