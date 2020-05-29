import json
import mistakes as error


class Comparator():

    def __init__(self):
        self.error_manager = error.FehlerManager()

    # funcname = name of the function. For example: example.func(), here func would be the funcname.
    # package = self explanatory
    # prefix = this is either the class or the file name. In the example above, "example" would be the prefix.
    # keywords = list of the given parameters.
    # line = line of the function call
    def compare(self, json_file, path, funcname, keywords, line, classname = None):
        # Load the json file which contains the class, function and method names.
        #with open(json_dir) as json_file:
        #    json_file = json.load(json_file)
        #json_file = json.loads(json_obj)

        function_found = False
        self.error_manager.fehler = []


        if classname is None:
            # Check for functions
            # If a class name is not given, then the function call is a "function", and no class needs to be checked.
            if path in json_file["function"].keys() and funcname in json_file["function"][path].keys():
                function_found = True
                for k in keywords:
                    if k not in json_file["function"][path][funcname]:
                        new_error = error.Fehler(path, line, "The parameter [" + k + "] is not found.")
                        self.error_manager.fehlerHinzufuegen(new_error)

        else:
            # Check for methods
            # If a class name is given, then the function call is a "method", then the method key needs to be checked.
            # There are two cases here, first case is the call is a standard method inside a class.
            # Then we simply do the following steps:
            # 1- Does the path exist in "method", 2- does the class name exist in this path, 3- does the method exist in
            # the class. Then we check for parameters.
            if path in json_file["method"].keys() and classname in json_file["method"][path].keys() and funcname in json_file["method"][path][classname].keys():
                function_found = True
                for k in keywords:
                    if k not in json_file["method"][path][classname][funcname]:
                        new_error = error.Fehler(path, line, "The parameter [" + k + "] is not found.")
                        self.error_manager.fehlerHinzufuegen(new_error)

            # Check for class decleration
            # The second case is, if the given class name is the same as the function name, then the call is an object
            # creation. In this case, 1- we check if the path is in "method", 2- check if the class is in the path,
            # 3- if the class name is the same as the function name, then we compare the keywords with the parameters of
            # the __init__ method (the constructor) in the class.

            if path in json_file["method"].keys() and classname in json_file["method"][path].keys():
                if classname == funcname:
                    function_found = True
                    for k in keywords:
                        if k not in json_file["method"][path][classname]["__init__"]:
                            new_error = error.Fehler(path, line, "The parameter [" + k + "] is not found.")
                            self.error_manager.fehlerHinzufuegen(new_error)

        if not function_found:
            function_not_found_error = error.Fehler("", line, "The function [" + funcname + "] or the path [" + path + "] does not exist.")
            self.error_manager.fehlerHinzufuegen(function_not_found_error)
            self.error_manager.printFehlerList()
            return 1

        if not self.error_manager.fehler == []:
            self.error_manager.printFehlerList()

        return 0

   # def beispiel(self, json_file, path, funcname, unbenannte, keywords, line, classname = None):
        # keywords = benannte argumente namen LIST
        # unbenannte = unbenannte argumente (wirkliche argumente) LIST
        # len(keywords) + len(unbenannte) = anzahl der verwendeten argumenten
        # vergleich das mit min-max bedingung
        # in hadys code there is info if a parameter has a default value or not
        # could be tupels (like [FUNCNAME, DEFAULT] or [FUNCNAME, NONE]
        # die Anzahl der Argumente die kein Default Wert haben = min

        # MIT DEFAULTS ZU ARBEITEN GEHÖRT AUCH DEM 3. USE CASE, z.B. vergleiche ob arg == default wert
        # def f(...,a = 1,...):
        #
        # f(...,a = 1,...): Shoul give warning that 1 is already the default argument.

     #   [funcname, None] -> 0. Index = funcname, None = hat kein Default wert