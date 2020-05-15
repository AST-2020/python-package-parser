import unittest

from experiments.unittest_test.my_math import fibonacci


class MyMathTestCase(unittest.TestCase):
    def test_fibonacci_returns_the_correct_result_for_nonnegative_values(self):
        # Base cases
        self.assertEqual(fibonacci(0), 0, "fibonacci(0) = 0")
        self.assertEqual(fibonacci(1), 1, "fibonacci(1) = 1")

        # Recursive case
        self.assertEqual(fibonacci(4), 3, "fibonacci(4) = 3")

    def test_fibonacci_raises_exception_for_negative_values(self):
        self.assertRaises(ValueError, lambda: fibonacci(-1))


if __name__ == '__main__':
    unittest.main()
