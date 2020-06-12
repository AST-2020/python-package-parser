import os


if __name__ == '__main__':
    print(os.listdir("TestDirectory"))

    for file in os.listdir("TestDirectory"):
        if file.endswith(".py"):
            # print(os.path.join("/TestDirectory", file))
            py_file = file.replace("py", "pyi")
            directory = os.listdir("TestDirectory")
            if file.replace("py", "pyi") in os.listdir("TestDirectory") or file.replace("py", "pyi.in") in os.listdir("TestDirectory"):
                print(os.path.join("/TestDirectory", file.replace("py", "pyi.in")))
