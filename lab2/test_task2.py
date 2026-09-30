"""Модульные тесты для task2.py."""
import unittest

from task2 import (compose, mean, median, normalize, normalize_inplace,
                   pipeline, variance)


class TestStatistics(unittest.TestCase):
    def test_mean(self):
        self.assertAlmostEqual(mean([1, 2, 3, 4]), 2.5)

    def test_single_element(self):
        self.assertEqual(mean([7]), 7)
        self.assertEqual(variance([7]), 0)
        self.assertEqual(median([7]), 7)

    def test_negative_numbers(self):
        self.assertAlmostEqual(mean([-3, -1, 1, 3]), 0)
        self.assertAlmostEqual(variance([-3, -1, 1, 3]), 5)
        self.assertEqual(median([-5, -1, -3]), -3)

    def test_empty_list(self):
        with self.assertRaises(ValueError):
            mean([])
        with self.assertRaises(ValueError):
            median([])

    def test_median_even(self):
        self.assertEqual(median([4, 1, 3, 2]), 2.5)


class TestHigherOrder(unittest.TestCase):
    def test_compose_order(self):
        f = compose(lambda x: x + 1, lambda x: x * 2)
        self.assertEqual(f(5), 11)  # (5 * 2) + 1

    def test_compose_empty(self):
        self.assertEqual(compose()(42), 42)

    def test_pipeline_order(self):
        self.assertEqual(pipeline(5, lambda x: x + 1, lambda x: x * 2), 12)


class TestPurity(unittest.TestCase):
    def test_normalize_is_pure(self):
        data = [2, 4, 6]
        self.assertEqual(normalize(data), [0.0, 0.5, 1.0])
        self.assertEqual(data, [2, 4, 6])

    def test_normalize_inplace_mutates(self):
        data = [2, 4, 6]
        normalize_inplace(data)
        self.assertEqual(data, [0.0, 0.5, 1.0])


if __name__ == "__main__":
    unittest.main()
