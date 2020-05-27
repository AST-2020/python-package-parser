import comparator
import unittest

class TestComparator(unittest.TestCase):



    # With this assertion, the comparison should be true
    # That means, all functions, methods, parameters etc. must be found
    def test_compare(self):
        # Testing the compare method
        comp = comparator.Comparator()
        f_names = ["car.Car", "myCar.get_info", "myCar.drive", "car.play_music"]
        p_names = [[], [], ['speed'], ['song_name', 'artist']]

        for f in range(len(f_names)):
            result = comp.compare(f_names[f], p_names[f], "test_dir/functions_and_methods.json")
            self.assertEqual(0, result)




if __name__ == "__main__":
    unittest.main()