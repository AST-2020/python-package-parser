from library_model import Library, Module, Class, Function

if __name__ == '__main__':

    # um zu die geparsete Daten zu erhalten (VIP)
    package = Library([])
    package.convert_to_python("results_TestDirectory.json")
    # print(package)

    print("one way to get information about the parameters of a function:\n")
    # function = package.get_top_level_function("TestDirectory.file1", "testFunc1")
    # function_parameters = function.get_parameters()
    # print(function_parameters, "\n")
    # for parameter in function_parameters:
    #     print(function.get_parameter(parameter).get_name()," ", function.get_parameter(parameter).has_default(), " ",
    #           function.get_parameter(parameter).get_default())

    print("one way to get information about the parameters of a method: (more details)\n")
    # method = package.get_method("TestDirectory.file1", "testFile1", "__init__")
    # print(method)
    #
    # method_parameters = method.get_parameters()
    # # wir brauchen den Keys, weil die Parameter Objekten sind unter keys gespeichert
    # print("to get all parameter keys (same as name): ", method_parameters, "\n")
    #
    # for parameter in method_parameters:
    #     print("the method and its default value: (", method.get_parameter(parameter), ")")
    #     print("name: ", method.get_parameter(parameter).get_name(), "\ndoes it has a default value:",
    #           method.get_parameter(parameter).has_default(), "\nthe default value: ",
    #           method.get_parameter(parameter).get_default(), "\n")
    #
    #

    print("more methods shown in details")
    # package = Library([])
    # package.convert_to_python("results_TestDirectory.json")


# um alle Modulen in einem Paket zu bekommen (nicht Objekten, sondern keys)
    # modules = package.get_modules()
    # print(package.get_modules())

# um eine Module zurückzubekommen, gegeben entweder das Index von dem Module in dem List von Keys, oder die name
# vom Modul
    # module: Module = package.get_module(modules[6])
    # # print(module)
    # module: Module = package.get_module("TestDirectory.file1")
    # # print(module)

# um alle klassen in einem Modul zu bekommen (die reste sind ähnlich wie beim Modul
    # classes = module.get_classes()
    # print(classes)

# (die geliche für Funktionen)
    # functions = module.get_top_level_functions()
    # # print(functions)
    #
    # function: Function = module.get_top_level_function("testFunc1")
    # # print(function)
    #
    # function: Function = module.get_top_level_function(functions[0])
    # # print(function)

# die gleiche für Pararmetern
    # function_parameters = function.get_parameters()
    # # print(function_parameters, "\n")
    #

##### VIP ########
# wie man mit dem Schlüssel den Objekt bekommmen kann (parameter in diesem Fall) (nicht so Kompakt)
# for Loop is bevorzügt (das ist nur für Erklärung)
    # # print(function.get_parameter(function_parameters[1]).get_name())
    # # print(function.get_parameter(function_parameters[1]).has_default())
    # # print(function.get_parameter(function_parameters[1]).get_default(), "\n")
    #

