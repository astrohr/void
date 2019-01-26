import os
import unittest
from unittest import mock

import docopt

from void import math_utils

class CalculatePolyTest(unittest.TestCase):
	def test_calculate_poly(self):
		values = math_utils.calculate_poly((0, 0), 3, 3, 315)
		expected = [[-1.29893408e-16, -2.12132034e+00],
 					[-2.12132034e+00,  0.00000000e+00],
 					[ 1.29893408e-16,  2.12132034e+00],
 					[ 2.12132034e+00,  0.00000000e+00]]
		self.assertEqual(expected, values)
