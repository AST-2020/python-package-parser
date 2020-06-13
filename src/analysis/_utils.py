from typing import Optional, List

from analysis.message import Message
from library.model import Package, Parameter, Function


def get_parameters(package: Package, module_path: str, func_name: str, cls_name: str) -> Optional[List[Parameter]]:
    overloads = get_matching_overloads(package, module_path, func_name, cls_name)
    if len(overloads) != 1:
        return None
    else:
        return overloads[0].get_parameters()


def get_matching_overloads(package: Package, module_path: str, func_name: str,
                           cls_name: Optional[str]) -> List[Function]:
    if _is_constructor_call(package, module_path, func_name, cls_name):
        return package.get_methods_with_name(module_path, func_name, "__init__")
    elif _is_method_call(package, module_path, func_name, cls_name):
        return package.get_methods_with_name(module_path, cls_name, func_name)
    else:
        return package.get_top_level_functions_with_name(module_path, func_name)


def function_not_found_error(func_name: str, file: str, line: int) -> Message:
    return Message(file, line, f"Function/method '{func_name}' was not found.")


def qualified_name(import_path: str, func_name: str):
    return f"{import_path}.{func_name}"


def _is_constructor_call(package: Package, module_path: str, func_name: str, cls_name: str) -> bool:
    return len(package.get_classes_with_name(module_path, func_name)) > 0 or \
           cls_name is not None and func_name == cls_name


def _is_method_call(package: Package, module_path: str, func_name: str, cls_name: Optional[str]) -> bool:
    return not _is_constructor_call(package, module_path, func_name, cls_name) and cls_name is not None
