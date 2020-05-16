import unittest

from experiments.unittest_test.my_math import fibonacci, factorial, collatz


class MyMathTestCase(unittest.TestCase):
    def test_fibonacci_returns_the_correct_result_for_nonnegative_values(self):
        # Base cases
        self.assertEqual(fibonacci(0), 0, "fibonacci(0) = 0")
        self.assertEqual(fibonacci(1), 1, "fibonacci(1) = 1")

        # Recursive case
        self.assertEqual(fibonacci(4), 3, "fibonacci(4) = 3")

    def test_fibonacci_raises_exception_for_negative_values(self):
        self.assertRaises(ValueError, lambda: fibonacci(-1))

    def test_factorial_returns_the_correct_result_for_nonnegative_values(self):
        # Base cases
        self.assertEqual(factorial(0), 1, "factorial(0) = 1")

        # Recursive case
        self.assertEqual(factorial(3), 6, "factorial(3) = 6")

    def test_factorial_raises_exception_for_negative_values(self):
        self.assertRaises(ValueError, lambda: factorial(-1))


if __name__ == '__main__':
    unittest.main()
