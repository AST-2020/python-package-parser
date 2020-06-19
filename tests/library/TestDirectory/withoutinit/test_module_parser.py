import unittest
from unittest import TestCase
from src.library.parser import _module_parser


class Test(TestCase):
    def test__find_parameter_hint_epy_style(self):
        eingabe = """
         This is a javadoc style.

         @param param1: this is a first param
         @param param2: this is a second param
         @return: this is a description of what is returned
         @raise keyError: raises an exception
         """
        result = [('param1', 'this is a first param'), ('param2', 'this is a second param')]

        self.assertListEqual(result, _module_parser._find_parameter_hint_epy_style(eingabe))

    def test__find_parameter_hint_google_style(self):
        eingabe = """
        This is an example of Google style.
        
        Args:
            param1: This is a first param
            param2: This is a second param
        
        Returns:
            This is a description of what is returned.
        
        Raises:
            KeyError: Raises an exception.
        """

        result = [("param1", "This is a first param"), ("param2", "This is a second param")]

        self.assertListEqual(result, _module_parser._find_parameter_hint_google_style(eingabe))

    def test__find_parameter_hint_numpydoc_style(self):
        eingabe = """
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
        """

        result = [("first", "array_like"), ("second", ""), ("third", "{'value', 'other'}, optional")]

        self.assertListEqual(result, _module_parser._find_parameter_hint_numpydoc_style(eingabe))

    def test__find_parameter_hint_rest_style(self):
        eingabe = """
        This is a reST style.

        :param param1: this is a first param
        :param param2: this is a second param
        :returns: this is a description of what is returned
        :raises keyError: raises an exception
        """

        result = [("param1", "this is a first param"), ("param2", "this is a second param")]

        self.assertListEqual(result, _module_parser._find_parameter_hint_rest_style(eingabe))

if  __name__ =='__main__':
    unittest.main()