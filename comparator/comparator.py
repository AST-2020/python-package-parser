import json

class Comparator():

    def compare(self, name, keywords, json_dir):
        # Load the json file which contains the class, function and method names.
        with open(json_dir) as json_file:
            json_file = json.load(json_file)

            # In Marwin's code, the method & function names are stored like this:
            # example_class.example_method (or file_name.example_function)
            # We need to separate the file/class name from the function/method name.
            function_name = name.split(".") # Separate the function call in parts.
            function_found = False          # If the function is not there after checking function and method keys,
                                            # this will stay false and an error message will be shown.

            # Check if the call is a function
            for key in json_file["function"].keys():
                if key.endswith(function_name[0]) and function_name[1] in json_file["function"][key].keys():
                    print("The function (" + function_name[1] + ") is found.")
                    function_found = True
                    for parameter in keywords:
                        if parameter in json_file["function"][key][function_name[1]]:
                            print("Parameter (" + parameter + ") found in (" + key + "." + function_name[0] + ").")
                        else:
                            print("The parameter (" + parameter + ") was not found!")

            # Check if the call is a class decleration
            for key in json_file["method"].keys():
                if key.endswith(function_name[0]) and function_name[1] in json_file["method"][key].keys():
                    print("Class decleration (" + function_name[0] + ") found in (" + key + "." + function_name[0] + ").")
                    function_found = True
                    for parameter in keywords:
                        if parameter in json_file["method"][key][function_name[1]]["__init__"]:
                            print("Parameter (" + parameter + ") found in (" + key + "." + function_name[1] + ".__init__).")
                        else:
                            print("The parameter (" + parameter + ") was not found!")

            # Check if the call is a method in an already declared class
            for key in json_file["method"].keys():
                for c in json_file["method"][key].keys():
                    if function_name[1] in json_file["method"][key][c]:
                        print("Method (" + function_name[1] + ") found in (" + key + "." + c + ").")
                        function_found = True
                        for parameter in keywords:
                            if parameter in json_file["method"][key][c][function_name[1]]:
                                print("Parameter (" + parameter + ") found in (" + key + "." + c + "." + function_name[1] + ").")
                            else:
                                print("The parameter (" + parameter + ") was not found!")

            if not function_found:
                print("The function (" + name + ") does not exist!")
                return 1

            return 0
