from typing import List


def compare(code_line, data_structure, path_till_file, func_or_method_name, user_params, cls_name=None):
    # means a function was called
    if cls_name is None:
        if path_till_file in data_structure["function"] and func_or_method_name \
                in data_structure["function"][path_till_file]:
            args = data_structure["function"][path_till_file][func_or_method_name]

    else:
        if path_till_file in data_structure["method"] and cls_name in data_structure["method"][path_till_file] \
                and func_or_method_name in data_structure["method"][path_till_file][cls_name]:
            args = data_structure["method"][path_till_file][cls_name][func_or_method_name]

    # then compare the args to the user_parameters
    # if any errors found call function from jonas's code
