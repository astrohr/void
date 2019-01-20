import unittest
from unittest import mock

import docopt

from void import common


class LogTests(unittest.TestCase):
    @mock.patch('void.common.logging')
    def test_configure_log(self, p_logging):
        common.configure_log('3')
        p_logging.basicConfig.assert_called_once_with(
            level=p_logging.INFO, format=common.LOG_FORMAT
        )

    @mock.patch('void.common.logging')
    def test_configure_log_unknown_cerbosity(self, *_):
        with self.assertRaises(docopt.DocoptExit):
            common.configure_log('321')
