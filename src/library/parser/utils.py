def find_type_hint(subscriptable_object, hint_string=""):
    if subscriptable_object is None or type(subscriptable_object) is str:
        return subscriptable_object
    if subscriptable_object.__dir__()[0] in ["id", "s"]:
        hint_string += getattr(subscriptable_object, subscriptable_object.__dir__()[0])
    elif subscriptable_object.__dir__()[0] == "value":
        hint = find_type_hint(subscriptable_object.value)
        if hint is not None:
            hint_string += hint
        else:
            hint_string += "type(None)"
    elif subscriptable_object is Ellipsis:
        hint_string += "ellipsis"

    if "slice" in subscriptable_object.__dir__() and "elts" not in subscriptable_object.slice.value.__dir__():
        hint_string += "[" + find_type_hint(subscriptable_object.slice.value) + "]"
    elif "slice" in subscriptable_object.__dir__():
        hint_string += find_type_hint(subscriptable_object.slice)
    elif "elts" in subscriptable_object.__dir__():
        hint_string += "["
        for i in range(len(subscriptable_object.elts)):
            if i < len(subscriptable_object.elts) - 1:
                hint_string += find_type_hint(subscriptable_object.elts[i]) + ", "
            else:
                hint_string += find_type_hint(subscriptable_object.elts[i])
        hint_string += "]"
    return hint_string
