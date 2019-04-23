import unittest

from void import math_utils


class CalculatePolyTest(unittest.TestCase):
    @staticmethod
    def _round(values, n):
        return [list(map(lambda x: round(x, n), x)) for x in values]

    def test_calculate_45(self):
        values = math_utils.calculate_poly((0, 0), 3, 3, 315)
        values = self._round(values, 4)
        expected = [[0, -2.1213], [-2.1213, 0], [0, 2.1213], [2.1213, 0]]
        self.assertSequenceEqual(values, expected)

    def test_calculate_0(self):
        values = math_utils.calculate_poly((0, 0), 3, 3, 0)
        values = self._round(values, 1)
        expected = [[-1.5, -1.5], [-1.5, 1.5], [1.5, 1.5], [1.5, -1.5]]
        self.assertSequenceEqual(values, expected)

    def test_calculate_90(self):
        values = math_utils.calculate_poly((0, 0), 3, 3, 90)
        values = self._round(values, 1)
        expected = [[-1.5, 1.5], [1.5, 1.5], [1.5, -1.5], [-1.5, -1.5]]
        self.assertSequenceEqual(values, expected)

    def test_calculate_rectangle(self):
        values = math_utils.calculate_poly((0, 0), 4, 2, 90)
        values = self._round(values, 0)
        expected = [[-1, 2], [1, 2], [1, -2], [-1, -2]]
        self.assertSequenceEqual(values, expected)
