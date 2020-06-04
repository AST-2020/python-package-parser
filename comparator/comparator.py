import json
import fehler.fehler as error
from library_model import Library, Module, Class, Function


class Comparator:

    def __init__(self, source):
        self.source = source
        self.error_manager = error.FehlerManager()

    def compare_arg_names(self, line, path, keywords, func_name, cls_name=None):
        self.error_manager.fehler = []
        # get args from source dict
        function_found = False
        args = []

        if cls_name is not None:
            # if constructor
            if func_name == cls_name:
                method = self.source.get_method(path, cls_name, "__init__")  # to get the object (type(Function)) back
                if method is not None:
                    function_found = True
                    args = method.get_parameters()
                else:
                    return
            else:
                method = self.source.get_method(path, cls_name, func_name)  # to get the object (type(Function)) back
                if method is not None:
                    function_found = True
                    args = method.get_parameters()

    # def get_top_level_function(self, module_path: str, function_name: str) -> Function:
        else:  # if function(parameters)
            function = self.source.get_top_level_function(path, func_name)  # to get the object (type(Function)) back
            if function is not None:
                function_found = True
                args = function.get_parameters()

        # compare keywords
        if function_found:
            for key in keywords:
                if key not in args:
                    new_error = error.Fehler(path + "." + func_name, line, "Parameter [" + key + "] not found.")
                    self.error_manager.fehlerHinzufuegen(new_error)

        else:
            function_not_found_error = error.Fehler("", line,
                                                    "The function [" + func_name + "] or the path [" + path + "] does not exist.")
            self.error_manager.fehlerHinzufuegen(function_not_found_error)
            self.error_manager.printFehlerList()
            return 1

        if not self.error_manager.fehler == []:
            self.error_manager.printFehlerList()

    def compare_arg_amount(self, line, path, func_name, keywords, arg_values, cls_name):
        self.error_manager.fehler = []  # Create empty error list
        # user_total_args: arguments given by the user
        user_total_args = len(keywords) + len(arg_values)  # Save total number of arguments given by the user

        # This case is for when class name is not present
        # That means we are working with a function, so the program calls related methods from Hady's code.
        if cls_name is None:
            func_or_method_args = self.source.get_top_level_function(path, func_name)
        else:
            func_or_method_args = self.source.get_method(path, cls_name, func_name)

        if func_or_method_args is None:
            new_error = error.Fehler("", line, "Function/method " + func_name + " not found.")
            self.error_manager.fehlerHinzufuegen(new_error)
            self.error_manager.printFehlerList()
            return

        max = len(func_or_method_args)

        function_or_method_parameters = func_or_method_args.get_parameters()  # Get the parameter list

        # Total number of parameters
        for p in function_or_method_parameters:
            if not func_or_method_args.get_parameter(p).has_default():
                min += 1  # For every parameter that does NOT have a default value, min increased by 1

        # If a function is found AND the number of given arguments is lower than min or greater than max, add error
        if user_total_args < min or user_total_args > max:
            new_error = error.Fehler("", line,
                                     "Wrong number of parameters (" + user_total_args + "). Max: " + max + " Min: " + min)
            self.error_manager.fehlerHinzufuegen(new_error)

        # Print errors.
        if not self.error_manager.fehler == []:
            self.error_manager.printFehlerList()

        return 0
