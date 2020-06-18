import unittest
from unittest import TestCase
from src.library.parser._module_parser import *
from src.library.parser._module_parser import _find_parameter_hint_epy_style, _find_parameter_hint_google_style, \
    _find_parameter_hint_numpydoc_style, _find_parameter_hint_rest_style


class Test(TestCase):
    def test__find_parameter_hint_epy_style(self):
        result =    """
                    This is a javadoc style.

                    @param param1: this is a first param
                    @param param2: this is a second param
                    @return: this is a description of what is returned
                    @raise keyError: raises an exception
                    """
        self.assertEqual(result, _find_parameter_hint_epy_style(result))

    def test__find_parameter_hint_google_style(self):
        result =    """
                    This is an example of Google style.

                    Args:
                        param1: This is the first param.
                        param2: This is a second param.

                    Returns:
                        This is a description of what is returned.

                    Raises:
                        KeyError: Raises an exception.
                    """
        self.assertEqual(result, _find_parameter_hint_google_style(result))

    def test__find_parameter_hint_numpydoc_style(self):
        result = """
                    My numpydoc description of a kind
                    of very exhautive numpydoc format docstring.

                    Parameters
                    ----------
                    first : array_like
                        the 1st param name `first`
                    second :
                        the 2nd param
                    third : {'value', 'other'}, optional
                        the 3rd param, by default 'value'

                    Returns
                    -------
                    string
                        a value in a string

                    Raises
                    ------
                    KeyError
                        when a key error
                    OtherError
                        when an other error
                    """
        self.assertEqual(result, _find_parameter_hint_numpydoc_style(result))

    def _test__find_parameter_hint_rest_style(self):
        result =    """
                    This is a reST style.

                    :param param1: this is a first param
                    :param param2: this is a second param
                    :returns: this is a description of what is returned
                    :raises keyError: raises an exception
                    """
        self.assertEqual(result, _find_parameter_hint_rest_style(result))

if  __name__ =='__main__':
    unittest.main()