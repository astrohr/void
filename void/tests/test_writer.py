import os
import unittest
from unittest import mock

import psycopg2

from void import common
from void.settings import settings
from void.writer import Writer, main


class WriterTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        env_path = os.path.join(os.path.dirname(__file__), 'tests.env')
        settings.load(env_path)

        with common.DataBase.get_pg_db(settings) as db:
            db.conn.set_isolation_level(0)
            db.exec(f'DROP DATABASE IF EXISTS {settings.POSTGRES_DB};')
            db.exec(f'CREATE DATABASE {settings.POSTGRES_DB};')
            db.conn.set_isolation_level(1)

        with common.DataBase.get_void_db(settings) as db:
            db.exec('DROP TABLE IF EXISTS observations;')
            db.exec('DROP EXTENSION IF EXISTS postgis CASCADE;')

    @classmethod
    def tearDownClass(cls):
        with common.DataBase.get_pg_db(settings) as db:
            db.conn.set_isolation_level(0)
            db.exec(f'DROP DATABASE {settings.POSTGRES_DB};')
            db.conn.set_isolation_level(1)

    @mock.patch('void.writer.Writer.create_table')
    def test_init(self, p_create_table):
        writer = Writer()
        p_create_table.assert_called_once_with()
        self.assertIsInstance(writer.db, common.DataBase)

    def test_create_table(self):
        with mock.patch.object(Writer, 'create_table'):
            writer = Writer()
        with common.DataBase.get_void_db(settings) as db:
            with self.assertRaises(psycopg2.ProgrammingError):
                db.exec('SELECT * FROM observations LIMIT 2')

        writer.create_table()
        writer.close()

        with common.DataBase.get_void_db(settings) as db:
            results = db.exec('SELECT * FROM observations LIMIT 2')
        self.assertIsNone(results)


class MainTests(unittest.TestCase):

    @mock.patch('void.writer.Writer')
    @mock.patch('void.writer.log')
    @mock.patch('void.writer.common')
    @mock.patch('void.writer.sys')
    @mock.patch('docopt.sys')
    def test_cli_args(self, p_docopt_sys, p_sys, p_common, *_):
        p_docopt_sys.argv = ['script.py', '-V', '3']
        p_sys.stdin = []
        main()
        p_common.configure_log.assert_called_once_with('3')

    @mock.patch('void.writer.Writer')
    @mock.patch('void.writer.common')
    @mock.patch('void.writer.docopt.docopt')
    @mock.patch('void.writer.log')
    @mock.patch('void.writer.sys')
    def test_sigint(self, p_sys, p_log, *_):
        mock_line = mock.MagicMock()
        mock_line.strip.side_effect = KeyboardInterrupt
        p_sys.stdin = [mock_line]
        main()
        self.assertIn(mock.call('SIGINT'), p_log.debug.call_args_list)

    @mock.patch('void.writer.common')
    @mock.patch('void.writer.docopt.docopt')
    @mock.patch('void.writer.Writer')
    @mock.patch('void.writer.sys')
    def test_empty_line(self, p_sys, p_writer_cls, *_):
        p_sys.stdin = ['line 1', '', 'line 3']
        main()
        writer = p_writer_cls.return_value
        expected = [mock.call('line 1'), mock.call('line 3')]
        self.assertEqual(expected, writer.insert_data.call_args_list)

    @mock.patch('void.writer.common')
    @mock.patch('void.writer.docopt.docopt')
    @mock.patch('void.writer.Writer')
    @mock.patch('void.writer.log')
    @mock.patch('void.writer.sys')
    def test_catch_exc(self, p_sys, p_log, p_writer_cls, *_):
        p_sys.stdin = ['line 1']
        writer = p_writer_cls.return_value
        writer.insert_data.side_effect = ValueError('foo')
        main()
        p_log.warning.assert_called_once_with('foo', exc_info=True)
