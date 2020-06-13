from typing import List

import messages.fehler as error
from library.model import Package


class Comparator:

    def __init__(self, package):
        self.package: Package = package
        self.FehlerManager = error.FehlerManager()

    def compare_arg_names(self, file: str, line: int, import_path: str, keyword_arguments: List[str], func_name, cls_name=None):
        self.FehlerManager.fehler = []
        # get args from source dict
        function_found = False
        args = []

        if len(self.package.get_classes_with_name(import_path, func_name)) == 1: # func_name ???
            if len(self.package.get_methods_with_name(import_path, func_name, "__init__")) == 1:
                method = self.package.get_methods_with_name(import_path, func_name, "__init__")[0]
                function_found = True
                args = method.get_parameters()
            else:
                function_found = True
                args = []
        elif cls_name is not None:
            if func_name == cls_name:
                cls_name = func_name
                method = self.package.get_methods_with_name(import_path, cls_name, "__init__")  # to get the object (type(Function)) back
                if len(method) == 1:
                    function_found = True
                    args = method[0].get_parameters()
                else:
                    return
            else:
                method = self.package.get_methods_with_name(import_path, cls_name, func_name)  # to get the object (type(Function)) back
                if len(method) == 1:
                    function_found = True
                    args = method[0].get_parameters()

        # def get_top_level_function(self, module_path: str, function_name: str) -> Function:
        else:  # if function(parameters)
            function = self.package.get_top_level_functions_with_name(import_path, func_name)  # to get the object (type(Function)) back
            if len(function) == 1:
                function_found = True
                args = function[0].get_parameters()

        # compare keywords
        if function_found:
            for key in keyword_arguments:
                if key not in args:
                    new_error = error.Fehler(import_path + "." + func_name, line, "Parameter [" + key + "] not found.", file)
                    self.FehlerManager.fehlerHinzufuegen(new_error)

        else:
            function_not_found_error = error.Fehler("", line,
                                                    "The function [" + func_name + "] or the path [" + import_path + "] does not exist.",
                                                    file)
            self.FehlerManager.fehlerHinzufuegen(function_not_found_error)
            self.FehlerManager.printFehlerList()
            return 1

        if not self.FehlerManager.fehler == []:
            self.FehlerManager.printFehlerList()

    def compare_arg_amount(self, file, line, path, func_name, keywords, arg_values, cls_name):
        self.FehlerManager.fehler = []  # Create empty error list
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
            new_error = error.Fehler(path + "." + func_name, line, "Function/method " + func_name + " not found.", file)
            self.FehlerManager.fehlerHinzufuegen(new_error)
            self.FehlerManager.printFehlerList()
            return

        max = len(func_or_method_args)
        min = 0

        # Total number of parameters
        for p in func_or_method_args:
            if not p.has_default():
                min += 1  # For every parameter that does NOT have a default value, min increased by 1

        # If a function is found AND the number of given arguments is lower than min or greater than max, add error
        if user_total_args < min or user_total_args > max:
            new_error = error.Fehler(path + "." + func_name, line,
                                     "Wrong number of parameters (" + str(user_total_args) + "). Max: " + str(max)
                                     + " Min: " + str(min), file)
            self.FehlerManager.fehlerHinzufuegen(new_error)

        # Print errors.
        if not self.FehlerManager.fehler == []:
            self.FehlerManager.printFehlerList()
        return 0
