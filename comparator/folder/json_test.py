import json


with open("test_dir/functions_and_methods.json") as json_file:
    json_file = json.load(json_file)

    print(json_file)
    print("function" in json_file)
    print("song_name" in json_file["function"]["test_dir.car"]["play_music"])

    for key in json_file:
        value = json_file[key]
        print("The key and value are {} = {}".format(key, value))

    print("-----------------")
    function_name = []
    function_name.append("car")
    function_name.append("play_music")
    function_json_dir = []
    keywords = ["song_name", "blabla"]
    print(json_file.keys())

    for key in json_file["function"].keys():
        if key.endswith(function_name[0]) and function_name[1] in json_file["function"][key].keys():
            print("The function (" + function_name[1] + ") is found.")
            for parameter in keywords:
                if parameter in json_file["function"][key][function_name[1]]:
                    print("Parameter (" + parameter + ") found in function (" + key + "." + function_name[1] + ").")
                else:
                    print("The parameter (" + parameter + ") does not exist in (" + key + "." + function_name[1] + ")!")

    for key in json_file["method"].keys():
        if key.endswith(function_name[0]) and function_name[1] in json_file["method"][key].keys():
            print("Class decleration (" + function_name[0] + ") found (" + key + "." + function_name[1] + ").")
            for parameter in keywords:
                if parameter in json_file["method"][key][function_name[1]]["__init__"]:
                    print("Parameter (" + parameter + ") found in (" + key + "." + function_name[1] + ".__init__).")

    for key in json_file["method"].keys():
        for c in json_file["method"][key].keys():
            if function_name[1] in json_file["method"][key][c]:
                print("Method (" + function_name[1] + ") found (" + key + "." + c + ").")
                for parameter in keywords:
                    if parameter in json_file["method"][key][c][function_name[1]]:
                        print("Parameter (" + parameter + ") found in (" + key + "." + c + "." + function_name[1] + ").")
