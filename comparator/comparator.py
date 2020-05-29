import json
import fehler.fehler as error


class Comparator():

    def __init__(self, source):
        self.source = source
        self.error_manager = error.FehlerManager()

    def compare_arg_names(self, line, path, func_name, keywords, cls_name):
        self.error_manager.fehler = []
        # get args from source dict
        function_found = False
        args = []

        if cls_name is None:
            # if constructor
            if (path in self.source['method']) and (func_name in self.source['method'][path]) \
                    and ('__init__' in self.source['method'][path][func_name]):
                function_found = True
                args = self.source['method'][path][func_name]['__init__']

            # if function
            elif (path in self.source['function']) and (func_name in self.source['function'][path]):
                function_found = True
                args = self.source['function'][path][func_name]
        else:
            # if method
            if (path in self.source['method']) and (cls_name in self.source['method'][path])\
                and (func_name in self.source['method'][path][cls_name]):
                function_found = True
                args = self.source['method'][path][cls_name][func_name]

        source_keywords = [item[0] for item in args]

        # compare keywords
        for key in keywords:
            if key not in source_keywords and function_found:
                new_error = error.Fehler(path + "." + func_name, line, "Parameter [" + key + "] not found.")
                self.error_manager.fehlerHinzufuegen(new_error)

        if not function_found:
            function_not_found_error = error.Fehler("", line, "The function [" + func_name + "] or the path [" + path + "] does not exist.")
            self.error_manager.fehlerHinzufuegen(function_not_found_error)
            self.error_manager.printFehlerList()
            return 1

        if not self.error_manager.fehler == []:
            self.error_manager.printFehlerList()