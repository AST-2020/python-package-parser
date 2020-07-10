
import unittest
from analysis.message import MessageManager
from code_analyzer import analyze_file
from library.parser import parse_packages

class Comperation(unittest.TestCase):

    def test_check_default_value(self):

        mm = MessageManager()
        analyze_file('example1.py', parse_packages(['torch', 'sklearn']), mm)
        act_str = mm.messages[0].__str__()

        print('aaaa__________', act_str)
        exp_str = "Warning in 'example1.py' (28:1):  in function 'fractional_max_pool3d_with_indices' the  value of the parameter 'output_size' is the same as default value."
        self.assertEqual(act_str, exp_str)


if __name__ == '__main__':
    unittest.main()

