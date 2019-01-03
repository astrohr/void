
import unittest

from void import sniffer


class SnifferTests(unittest.TestCase):

    def test_true(self):
        self.assertTrue(sniffer.Sniffer)
