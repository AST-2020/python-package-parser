import analysis
import unittest
import json

class TestComparator(unittest.TestCase):

    def test_compare(self):
        # Testing the compare method
        comp = analysis.Comparator()

        with open("resultsTorch.txt") as json_file:
            json_file = json.load(json_file)
        json_file = json.loads(json_file)

        test1 = comp.compare(json_file, "torch.__config__", "parallel_info", [], 30)
        test2 = comp.compare(json_file, "torch.__con2312313fig__", "parallexxl_info", [], 30)
        self.assertEqual(0, test1)
        self.assertEqual(1, test2)


if __name__ == "__main__":
    unittest.main()