import unittest

import numpy as np

from void import math_utils


class CalculatePolyTest(unittest.TestCase):
    @staticmethod
    def _round(values):
        return [list(map(lambda x: round(x, 4), x)) for x in values]

    def test_calculate_45(self):
        values = math_utils.calculate_poly((0, 0), 3, 3, 315)
        values = self._round(values)
        expected = [[0, -2.1213], [-2.1213, 0], [0, 2.1213], [2.1213, 0]]
        expected = np.asarray(expected)
        expected = math_utils.sort_ndarray(expected)
        try:
            np.testing.assert_almost_equal(values, expected, decimal=4)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    def test_calculate_0(self):
        values = math_utils.calculate_poly((0, 0), 3, 3, 0)
        values = self._round(values)
        expected = [[1.5, -1.5], [-1.5, 1.5], [1.5, 1.5], [-1.5, -1.5]]
        expected = np.asarray(expected)
        expected = math_utils.sort_ndarray(expected)
        try:
            np.testing.assert_almost_equal(values, expected, decimal=4)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    def test_calculate_90(self):
        values = math_utils.calculate_poly((0, 0), 3, 3, 90)
        values = self._round(values)
        expected = [[1.5, -1.5], [-1.5, 1.5], [1.5, 1.5], [-1.5, -1.5]]
        expected = np.asarray(expected)
        expected = math_utils.sort_ndarray(expected)
        try:
            np.testing.assert_almost_equal(values, expected, decimal=4)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)

    def test_calculate_rectangle(self):
        values = math_utils.calculate_poly((0, 0), 4, 2, 90)
        values = self._round(values)
        expected = [[1, -2], [-1, 2], [1, 2], [-1, -2]]
        expected = np.asarray(expected)
        expected = math_utils.sort_ndarray(expected)
        try:
            np.testing.assert_almost_equal(values, expected, decimal=4)
            res = True
        except AssertionError as err:
            res = False
            print(err)
        self.assertTrue(res)
