import json
import fehler as error

class Comparator():

    def __init__(self):
        self.error_manager = error.FehlerManager()


    def compare(self, name, keywords, line, json_dir):
        # Load the json file which contains the class, function and method names.
        json_file = {}
        with open('resultsPytorch.txt') as file:
            json_obj = json.load(file)
        json_file = json.loads(json_obj)

        #with open(json_dir) as json_file:
        #    json_file = json.load(json_file)

        # In Marwin's code, the method & function names are stored like this:
        # example_class.example_method (or file_name.example_function)
        # We need to separate the file/class name from the function/method name.
        function_name = name.split(".") # Separate the function call in parts.
        function_found = False          # If the function is not there after checking function and method keys,
                                        # this will stay false and an error message will be shown.
        self.error_manager.fehler = []

        # Check if the call is a function
        for pack in json_file['function'].keys():
                if function_name[-1] in json_file['function'][pack].keys():
                    print(json_file['function'][pack][function_name[-1]])
                    function_found = True
                    #print(json_file['function'][pack][function_name[-1]])
                    for parameter in keywords:
                        if parameter not in json_file['function'][pack][function_name[-1]]:
                            new_error = error.Fehler(pack + "." + function_name[-1], line, "Parameter [" + parameter + "] not found.")
                            self.error_manager.fehlerHinzufuegen(new_error)

        # Check if the call is a method
        for pack in json_file['method'].keys():
            for file in json_file['method'][pack].keys():
                if function_name[-1] in json_file['method'][pack][file]:
                    print(json_file['method'][pack][file][function_name[-1]])
                    function_found = True
                    for parameter in keywords:
                        if parameter not in json_file['method'][pack][file][function_name[-1]]:
                            new_error = error.Fehler(pack + "." + function_name[-1], line, "Parameter [" + parameter + "] not found.")
                            self.error_manager.fehlerHinzufuegen(new_error)

        # check if the call is a class constructor
        for pack in json_file['method'].keys():
            if function_name[-1].lower() in json_file['method'][pack].keys():

                function_found = True
                for parameter in keywords:
                    if parameter not in json_file["method"][pack][function_name[-1].lower()]:
                        new_error = error.Fehler(pack + "." + function_name[-1] + ".__init__", line, "Parameter [" + parameter + "] not found.")
                        self.error_manager.fehlerHinzufuegen(new_error)


        if not self.error_manager.fehler == []:
            self.error_manager.printFehlerList()

            return 0
