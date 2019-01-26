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

    @mock.patch('void.reducer.common')
    @mock.patch('void.reducer.docopt')
    @mock.patch('void.reducer.log')
    @mock.patch('void.reducer.sys')
    def test_main(self, p_sys, *_):
        p_sys.stdin = ['void/tests/data/test_unflagged.fit']
        reducer.main()
        expected_output = (
            '{"date_obs": "2019-01-09T04:47:09.360", '
            '"exposure": 60.0, "focus": 4408, "ra_center": 167.81972847, '
            '"dec_center": 63.3125430004, "x_deg_size": 0.73301928819258, '
            '"y_deg_size": 0.73463276991788, "pos_angle": 356.673098539}\n'
        )
        p_sys.stdout.write.assert_called_with(expected_output)


class ReadHeaderDataTests(unittest.TestCase):
    def test_read_header_data(self):
        data = reducer.read_header_data('void/tests/data/test_unflagged.fit')
        expected = {
            'date_obs': '2019-01-09T04:47:09.360',
            'dec_center': 63.3125430004,
            'exposure': 60.0,
            'focus': 4408,
            'pos_angle': 356.673098539,
            'ra_center': 167.81972847,
            'x_deg_size': 0.73301928819258,
            'y_deg_size': 0.73463276991788
        }
        self.assertDictEqual(expected, data)


class EncodeHeaderDataTests(unittest.TestCase):
    def test_encode_header_data(self):
        encoded = reducer.encode_header_data({'foo': 123})
        expected = '{"foo": 123}'
        self.assertEqual(expected, encoded)
