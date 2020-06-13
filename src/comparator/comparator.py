from typing import List, Optional

from library.model import Package, Parameter
from messages import MessageManager, Message


class Comparator:

    def __init__(self, package):
        self.package: Package = package
        self.messageManager = MessageManager()

    def compare_arg_names(self, file: str, line: int, import_path: str, keyword_arguments: List[str], func_name,
                          cls_name=None):
        self.messageManager.clear()

        parameters = self.get_parameters(import_path, func_name, cls_name)
        if parameters is None:
            function_not_found_error = Message("", line,
                                               "The function [" + func_name + "] or the path [" + import_path + "] does not exist.",
                                               file)
            self.messageManager.addMessage(function_not_found_error)
            self.messageManager.printMessages()
            return 1

        param_names = [parameter.get_name() for parameter in parameters]

        for key in keyword_arguments:
            if key not in param_names:
                new_error = Message(import_path + "." + func_name, line, "Parameter [" + key + "] not found.", file)
                self.messageManager.addMessage(new_error)

        self.messageManager.printMessages()

    def get_parameters(self, import_path, func_name, cls_name) -> Optional[List[Parameter]]:
        if len(self.package.get_classes_with_name(import_path, func_name)) == 1:  # func_name ???
            if len(self.package.get_methods_with_name(import_path, func_name, "__init__")) == 1:
                method = self.package.get_methods_with_name(import_path, func_name, "__init__")[0]
                return method.get_parameters()
            else:
                return []  # TODO Should this not be None?
        elif cls_name is not None:
            if func_name == cls_name:
                cls_name = func_name
                method = self.package.get_methods_with_name(import_path, cls_name, "__init__")
                if len(method) == 1:
                    return method[0].get_parameters()
                else:
                    return None
            else:
                method = self.package.get_methods_with_name(import_path, cls_name, func_name)
                if len(method) == 1:
                    return method[0].get_parameters()

        else:
            function = self.package.get_top_level_functions_with_name(import_path, func_name)
            if len(function) == 1:
                return function[0].get_parameters()

    def compare_arg_amount(self, file, line, path, func_name, keywords, arg_values, cls_name):
        self.messageManager.clear()
        # user_total_args: arguments given by the user
        user_total_args = len(keywords) + len(arg_values)  # Save total number of arguments given by the user

        # This case is for when class name is not present
        # That means we are working with a function, so the program calls related methods from Hady's code.
        func_or_method_args = None

        if cls_name is None:
            func_or_method = self.package.get_top_level_functions_with_name(path, func_name)
            if len(func_or_method) == 1:
                func_or_method_args = func_or_method[0].get_parameters()
            else:
                return
        else:
            func_or_method = self.package.get_methods_with_name(path, cls_name, func_name)
            if len(func_or_method) == 1:
                func_or_method_args = func_or_method[0].get_parameters()

        if func_or_method_args is None:
            new_error = Message(path + "." + func_name, line, "Function/method " + func_name + " not found.", file)
            self.messageManager.addMessage(new_error)
            self.messageManager.printMessages()
            return

        max = len(func_or_method_args)
        min = 0

        # Total number of parameters
        for p in func_or_method_args:
            if not p.has_default():
                min += 1  # For every parameter that does NOT have a default value, min increased by 1

        # If a function is found AND the number of given arguments is lower than min or greater than max, add error
        if user_total_args < min or user_total_args > max:
            new_error = Message(path + "." + func_name, line,
                                "Wrong number of parameters (" + str(user_total_args) + "). Max: " + str(max)
                                + " Min: " + str(min), file)
            self.messageManager.addMessage(new_error)

        # Print errors.
        if not self.messageManager.fehler == []:
            self.messageManager.printMessages()
        return 0
