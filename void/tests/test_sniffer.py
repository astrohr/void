import os
import unittest
from unittest import mock

import docopt

from void import sniffer


class MainTests(unittest.TestCase):
    @mock.patch('void.sniffer.Sniffer')
    @mock.patch('void.sniffer.common')
    @mock.patch('void.sniffer.docopt')
    def test_main_init_sniffer(self, p_docopt, p_common, p_sniffer_class):
        mock_args = {
            'SEARCH_DIR': 'foo',
            '--tmin': 'bar',
            '--tmax': 'baz',
            '--maxn': 'omgwhatcomesafterbaz',
            '--flag': None,
            '--dry-run': False,
            '--verbosity': 789,
        }
        expected_call_kwargs = {
            'search_dir': 'foo',
            'tmin': 'bar',
            'tmax': 'baz',
            'maxn': 'omgwhatcomesafterbaz',
            'flag_name': None,
            'update_flag': True,
        }
        p_docopt.docopt.return_value = mock_args.copy()
        sniffer.main()
        p_sniffer_class.assert_called_once_with(**expected_call_kwargs)
        p_common.configure_log.assert_called_once_with(789)

    @mock.patch('void.sniffer.common')
    @mock.patch('void.sniffer.docopt')
    @mock.patch('void.sniffer.Sniffer')
    @mock.patch('void.sniffer.sys')
    def test_main_init_writes_files(self, p_sys, p_sniffer_class, *_):
        mock_fits = (item for item in (11, 22, 33, 44))
        expected_calls = [
            mock.call('11\n'),
            mock.call('22\n'),
            mock.call('33\n'),
            mock.call('44\n'),
        ]
        p_sniffer = p_sniffer_class.return_value
        p_sniffer.find_fits.return_value = mock_fits
        sniffer.main()
        self.assertEqual(expected_calls, p_sys.stdout.write.mock_calls)

    @mock.patch('docopt.sys')
    def test_unknown_cli_arg(self, p_sys):
        p_sys.argv = ['void_sniffer', '-foobar']
        with self.assertRaises(docopt.DocoptExit):
            sniffer.main()


@mock.patch('void.sniffer.fits.writeto')
class SnifferTests(unittest.TestCase):
    def setUp(self):
        base_dir = os.path.dirname(__file__)
        self.kwargs = {'search_dir': base_dir, 'maxn': None, 'tmin': None}

    def test_all_files_no_flag(self, p_writeto):
        self.kwargs['flag_name'] = None
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = [
            'void/tests/data/test2_flagged.fit',
            'void/tests/data/test_unflagged.fit',
            'void/tests/data/sub/test_in_sub_unflagged.fit',
        ]
        self.assertListEqual(expected, value)
        p_writeto.assert_not_called()

    def test_all_files_disabled_flag(self, p_writeto):
        self.kwargs['flag_name'] = '0'
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = [
            'void/tests/data/test2_flagged.fit',
            'void/tests/data/test_unflagged.fit',
            'void/tests/data/sub/test_in_sub_unflagged.fit',
        ]
        self.assertListEqual(expected, value)
        p_writeto.assert_not_called()

    def test_all_files_new_flag(self, p_writeto):
        self.kwargs['flag_name'] = 'foo'
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = [
            'void/tests/data/test2_flagged.fit',
            'void/tests/data/test_unflagged.fit',
            'void/tests/data/sub/test_in_sub_unflagged.fit',
        ]
        self.assertListEqual(expected, value)
        self.assertEqual(expected[0], p_writeto.mock_calls[0][1][0])
        self.assertEqual(expected[1], p_writeto.mock_calls[1][1][0])
        self.assertEqual(expected[2], p_writeto.mock_calls[2][1][0])

    def test_all_files_known_flag(self, p_writeto):
        self.kwargs['flag_name'] = 'VISNJAN'
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = [
            'void/tests/data/test_unflagged.fit',
            'void/tests/data/sub/test_in_sub_unflagged.fit',
        ]
        self.assertListEqual(expected, value)
        self.assertEqual(expected[0], p_writeto.mock_calls[0][1][0])
        self.assertEqual(expected[1], p_writeto.mock_calls[1][1][0])

    def test_maxn(self, p_writeto):
        self.kwargs['flag_name'] = '0'
        self.kwargs['maxn'] = 2
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = [
            'void/tests/data/test2_flagged.fit',
            'void/tests/data/test_unflagged.fit',
        ]
        self.assertListEqual(expected, value)
        p_writeto.assert_not_called()

    def test_min_time(self, p_writeto):
        self.kwargs['flag_name'] = '0'
        self.kwargs['tmin'] = '2019-01-01T00:00:00'
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = ['void/tests/data/test_unflagged.fit']
        self.assertListEqual(expected, value)
        p_writeto.assert_not_called()

    def test_max_time(self, p_writeto):
        self.kwargs['flag_name'] = '0'
        self.kwargs['tmax'] = '2019-01-01T00:00:00'
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = [
            'void/tests/data/test2_flagged.fit',
            'void/tests/data/sub/test_in_sub_unflagged.fit',
        ]
        self.assertListEqual(expected, value)
        p_writeto.assert_not_called()

    def test_max_time_only_date(self, p_writeto):
        self.kwargs['flag_name'] = '0'
        self.kwargs['tmax'] = '2019-01-01'
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = [
            'void/tests/data/test2_flagged.fit',
            'void/tests/data/sub/test_in_sub_unflagged.fit',
        ]
        self.assertListEqual(expected, value)
        p_writeto.assert_not_called()

    def test_time_range(self, p_writeto):
        self.kwargs['flag_name'] = '0'
        self.kwargs['tmax'] = '2017-12-01T00:00:00'
        self.kwargs['tmin'] = '2017-01-01T00:00:00'
        instance = sniffer.Sniffer(**self.kwargs)
        value = list(instance.find_fits())
        expected = ['void/tests/data/sub/test_in_sub_unflagged.fit']
        self.assertListEqual(expected, value)
        p_writeto.assert_not_called()
