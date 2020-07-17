from typing import List

dictionary = {
    "key": {
        "nested": [1, 2, 3]
    }
}


def get(data, path: List):
    # if len(path) == 0:
    #     return data
    #
    # if (isinstance(data, list) or isinstance(data, dict)) and path[0] in data:
    #     return get(data[path[0]], path[1:])
    # else:
    #     return None

    return call_function(data, path, lambda entry: entry)


def set(data, path: List, value):
    if len(path) == 0:
        return

    if (isinstance(data, list) or isinstance(data, dict)) and path[0] in data:
        if len(path) == 1:
            data[path[0]] = value
        else:
            set(data[path[0]], path[1:], value)


def call_function(data, path: List, f):
    if len(path) == 0:
        return

    if (isinstance(data, list) or isinstance(data, dict)) and path[0] in data:
        if len(path) == 1:
            return f(data[path[0]])
        else:
            return call_function(data[path[0]], path[1:], f)


print(get(dictionary, ["key", "nested", 2]))
set(dictionary, ["key", "nested", 2], 42)
print(get(dictionary, ["key", "nested", 2]))

call_function(dictionary, ["key", "nested"], lambda lst: lst.extend([4, 5, 6]))
call_function(dictionary, ["key", "nested"], lambda lst: print(lst))

