import os
import psycopg2
import sys
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
