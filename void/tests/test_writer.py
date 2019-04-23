import os
import psycopg2
import unittest
from unittest import mock

from void import common
from void.settings import settings
from void.writer import Writer


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

    def test_decode_data(self):
        writer = Writer()
        input_str = '{"foo": "bar"}'
        expected = {'foo': 'bar'}
        actual = writer.decode_data(input_str)
        self.assertEqual(expected, actual)

    def test_poly_to_linestr(self):
        writer = Writer()
        poly = [[1, 2], [3, 4], [5, 6]]
        date_tstamp = 30
        expected = "1 2 30,3 4 30,5 6 30,1 2 30"
        actual = writer.poly_to_linestr(date_tstamp, poly)
        self.assertEqual(expected, actual)

    def test_insert_data(self):
        writer = Writer()
        with common.DataBase.get_void_db(settings) as db:
            db.exec('TRUNCATE TABLE observations;')
        data_str = (
            '{"path": '
            '"/home/patrik/Workspace/void/void/tests/data/test2_flagged.fit", '
            '"date_obs": "2018-12-26T18:41:49.300", '
            '"exposure": 60.0, "observer": "", '
            '"polygon": [[23.120172630110357, 30.275351191536046], '
            '[23.080000853796616, 31.00642256430581], '
            '[23.808858702289644, 31.046472709263952], '
            '[23.849030478603385, 30.315401336494187]]}'
        )
        writer.insert_data(data_str)
        with common.DataBase.get_void_db(settings) as db:
            db.exec('SELECT * FROM observations')
            records = db.cursor.fetchall()
            self.assertIsNotNone(records)
