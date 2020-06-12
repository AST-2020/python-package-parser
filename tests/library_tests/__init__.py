from tests.library_tests import TestDirectory
from library.library_model import Library
from library.package_parser import read_directory


if __name__ == '__main__':

    library = TestDirectory.__file__
    library = library.replace("__init__.py", '')
    library = library[0:-1]
    path_to_delete = library.rsplit('TestDirectory', 1)[0]
    parsed_data = Library([])
    read_directory(library, path_to_delete, parsed_data)
    test_json_object = parsed_data.convert_to_json("TestDirectory")
