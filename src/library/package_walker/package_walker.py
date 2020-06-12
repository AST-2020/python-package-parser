import importlib
import inspect
import os

from pathlib import Path
from typing import Any, Generator, List, Optional, Tuple


def walk_package(package_name: str) -> Generator[Tuple[str, str, Optional[str]], Any, None]:
    """
    Yields 3-tuples of the form (module_path, python_file, python_interface_file), which can be iterated in a
    for-loop.

    Example of usage:
        for module_path, python_file, python_interface_file in walk_package("torch"):
            print(module_path, python_file, python_interface_file)

    Example of a tuple: (
        "torch.optim.adam",
        "C:/Anaconda/envs/ml/lib/site-packages/torch/optim/adam.py",
        "C:/Anaconda/envs/ml/lib/site-packages/torch/optim/adam.pyi"
    )
    """

    # Get package root
    package_root = _get_package_root(package_name)
    if package_root is None:
        print(f"Cannot find root of package {package_name}.")
        return

    # Walk through directories
    for dirpath, dirnames, filenames in os.walk(package_root):
        if "__pycache__" in dirnames:
            dirnames.remove("__pycache__")

        module_base_path = _get_module_base_path(package_name, package_root, dirpath)

        # Walk over Python files in directory
        for filename in filter(_is_python_file, filenames):
            module_path = _get_module_path(module_base_path, filename)
            python_file = Path(dirpath, filename).as_posix()
            python_interface_file = _get_python_interface_file(dirpath, filenames, filename)
            yield module_path, python_file, python_interface_file


def _get_package_root(package_name: str) -> Optional[str]:
    try:
        package = importlib.import_module(package_name)
        init_file = Path(inspect.getfile(package))
        return str(init_file.parent)
    except ModuleNotFoundError:
        return None


def _is_package_installed(package_name: str) -> bool:
    return _get_package_root(package_name) is not None


def _get_module_base_path(package_name: str, package_root: str, dirpath: str) -> str:
    module_base_path = package_name
    relative_dirpath = Path(dirpath).relative_to(package_root).as_posix()
    if relative_dirpath != ".":
        module_base_path += "." + str(relative_dirpath).replace("/", ".")
    return module_base_path


def _is_python_file(filename: str) -> bool:
    return Path(filename).suffix == ".py"


def _get_module_path(module_base_path: str, filename: str) -> str:
    if filename == "__init__.py":
        return module_base_path
    else:
        return module_base_path + "." + Path(filename).stem


def _get_python_interface_file(dirpath: str, filenames: List[str], filename: str) -> Optional[str]:
    pyi_file = filename.replace(".py", ".pyi")
    if pyi_file in filenames:
        return Path(dirpath, pyi_file).as_posix()

    pyi_in_file = filename.replace(".py", ".pyi.in")
    if pyi_in_file in filenames:
        return Path(dirpath, pyi_in_file).as_posix()
