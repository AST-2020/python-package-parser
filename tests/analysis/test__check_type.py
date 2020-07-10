import unittest
from analysis.message import MessageManager
from code_analyzer import analyze_file
from library.parser import parse_packages

class Comperation(unittest.TestCase):

    def test_check_type(self):

        mm = MessageManager()
        analyze_file('example1.py', parse_packages(['torch', 'sklearn']), mm)
        act_str = mm.messages[0].__str__()

        # print('aaaa__________', act_str)
        exp_str = "Error in 'example1.py' (28:1): Function 'fractional_max_pool3d_with_indices' the type of  'output_size' is not correct."
        self.assertEqual(exp_str, act_str)


if __name__ == '__main__':
    unittest.main()