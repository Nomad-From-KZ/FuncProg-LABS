"""Модульные тесты для task3.py."""
import unittest

from task3 import log_calls, memoize, validate_types


class TestDecorators(unittest.TestCase):
    def test_log_calls_keeps_result_and_name(self):
        @log_calls
        def add(a, b):
            """Сумма."""
            return a + b
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add.__name__, "add")
        self.assertEqual(add.__doc__, "Сумма.")

    def test_validate_types_ok(self):
        @validate_types(x=int)
        def square(x):
            return x * x
        self.assertEqual(square(4), 16)

    def test_validate_types_error(self):
        @validate_types(x=int)
        def square(x):
            return x * x
        with self.assertRaises(TypeError):
            square("4")
        with self.assertRaises(TypeError):
            square(x=4.0)

    def test_memoize_calls_once(self):
        calls = []

        @memoize
        def f(a, b=1):
            calls.append(a)
            return a * b
        self.assertEqual(f(2, b=3), 6)
        self.assertEqual(f(2, b=3), 6)
        self.assertEqual(len(calls), 1)
        self.assertEqual(f(2, b=4), 8)
        self.assertEqual(len(calls), 2)


if __name__ == "__main__":
    unittest.main()
