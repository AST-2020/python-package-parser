from typing import Optional, List

from library.model import Package, Parameter, Function


def get_parameters(package: Package, import_path, func_name, cls_name) -> Optional[List[Parameter]]:
    overloads = get_matching_overloads(package, import_path, func_name, cls_name)
    if len(overloads) != 1:
        return None
    else:
        return overloads[0].get_parameters()


def get_matching_overloads(package: Package, import_path, func_name, cls_name) -> List[Function]:
    if is_constructor_call(package, import_path, func_name, cls_name):
        return package.get_methods_with_name(import_path, func_name, "__init__")
    elif cls_name is not None:
        return package.get_methods_with_name(import_path, cls_name, func_name)
    else:
        return package.get_top_level_functions_with_name(import_path, func_name)


def is_constructor_call(package: Package, import_path, func_name, cls_name):
    return len(package.get_classes_with_name(import_path, func_name)) > 0 or \
           cls_name is not None and func_name == cls_name
