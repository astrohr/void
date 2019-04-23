import unittest
from unittest import mock

from void import reducer


class MainTests(unittest.TestCase):
    @mock.patch('void.reducer.common')
    @mock.patch('void.reducer.docopt')
    @mock.patch('void.reducer.log')
    @mock.patch('void.reducer.sys')
    def test_main_empty(self, p_sys, p_log, *_):
        p_sys.stdin = []
        reducer.main()
        expected_calls = [mock.call('listening'), mock.call('EOF')]
        self.assertListEqual(expected_calls, p_log.debug.mock_calls)

    @mock.patch('void.reducer.common')
    @mock.patch('void.reducer.docopt')
    @mock.patch('void.reducer.log')
    @mock.patch('void.reducer.sys')
    @mock.patch('void.reducer.read_header_data')
    def test_main_sigint(self, p_read_header_data, p_sys, p_log, *_):
        p_read_header_data.side_effect = KeyboardInterrupt
        p_sys.stdin = ['mock/file.path']
        reducer.main()
        expected_calls = [mock.call('listening'), mock.call('SIGINT')]
        self.assertListEqual(expected_calls, p_log.debug.mock_calls)

    @mock.patch('void.reducer.common')
    @mock.patch('void.reducer.docopt')
    @mock.patch('void.reducer.log')
    @mock.patch('void.reducer.sys')
    @mock.patch('void.reducer.read_header_data')
    def test_main_exception(self, p_read_header_data, p_sys, p_log, *_):
        p_read_header_data.side_effect = ValueError('Foo!')
        p_sys.stdin = ['mock/file.path']
        reducer.main()
        expected_calls = [mock.call('Foo!', exc_info=True)]
        self.assertListEqual(expected_calls, p_log.warning.mock_calls)

    @mock.patch('void.reducer.common')
    @mock.patch('void.reducer.docopt')
    @mock.patch('void.reducer.log')
    @mock.patch('void.reducer.sys')
    @mock.patch('void.reducer.read_header_data')
    def test_main_empty_line(self, p_read_header_data, p_sys, *_):
        p_sys.stdin = ['mock/file.path1', '', 'mock/file.path2']
        p_read_header_data.return_value = {'mock': 'data'}
        reducer.main()
        expected_calls = [
            mock.call('mock/file.path1'),
            mock.call('mock/file.path2'),
        ]
        self.assertListEqual(expected_calls, p_read_header_data.mock_calls)

    @mock.patch('void.reducer.common')
    @mock.patch('void.reducer.docopt')
    @mock.patch('void.reducer.log')
    @mock.patch('void.reducer.sys')
    def test_main_file_not_found(self, p_sys, p_log, *_):
        p_sys.stdin = ['foo/bar.fit', 'void/foo.fit']
        reducer.main()
        expected_calls = [
            mock.call('FileNotFoundError: "foo/bar.fit"'),
            mock.call('FileNotFoundError: "void/foo.fit"'),
        ]
        self.assertListEqual(expected_calls, p_log.warning.mock_calls)
        p_sys.stdout.write.assert_not_called()

    @staticmethod
    @mock.patch('void.reducer.common')
    @mock.patch('void.reducer.docopt')
    @mock.patch('void.reducer.log')
    @mock.patch('void.reducer.sys')
    def test_main(p_sys, *_):
        p_sys.stdin = ['void/tests/data/test_unflagged.fit']
        reducer.main()
        expected_output = (
            '{"path": "void/tests/data/test_unflagged.fit", '
            '"date_obs": "2019-01-09T04:47:09.360", "exposure": 60.0, '
            '"observer": "", '
            '"polygon": [[167.47515289626557, 62.92457609477469], '
            '[167.4325201282204, 63.65797077277967], '
            '[168.2069368117796, 62.967115228020326], '
            '[168.16430404373443, 63.7005099060253]]}\n'
        )
        p_sys.stdout.write.assert_called_with(expected_output)


class ReadHeaderDataTests(unittest.TestCase):
    def test_read_header_data(self):
        data = reducer.read_header_data('void/tests/data/test_unflagged.fit')
        expected = {
            'path': 'void/tests/data/test_unflagged.fit',
            'date_obs': '2019-01-09T04:47:09.360',
            'exposure': 60.0,
            'observer': '',
            'polygon': [
                [167.475_152_896_265_57, 62.924_576_094_774_69],
                [167.432_520_128_220_4, 63.657_970_772_779_67],
                [168.206_936_811_779_6, 62.967_115_228_020_326],
                [168.164_304_043_734_43, 63.700_509_906_025_3],
            ],
        }
        self.assertDictEqual(expected, data)


class EncodeHeaderDataTests(unittest.TestCase):
    def test_encode_header_data(self):
        encoded = reducer.encode_header_data({'foo': 123})
        expected = '{"foo": 123}'
        self.assertEqual(expected, encoded)
