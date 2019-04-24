import os
import unittest

from void import common
from void.settings import settings
from void.writer import Writer

# Test polygons
P_1 = [[2, 2], [-2, 2], [-2, -2], [2, -2]]
P_2 = [[7, 2], [3, 2], [3, -2], [7, -2]]
P_3 = [[2, -3], [-2, -3], [-2, -7], [2, -7]]

# Test timestamps
T_1 = 1_556_100_448
T_2 = 1_556_104_020

EXP = 5
OBSERVER = 'a'


class SelectorTests(unittest.TestCase):
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
            db.exec('TRUNCATE TABLE observations;')
            with Writer() as writer:
                paths = ['P_1', 'P_2', 'P_3', 'R_1']
                polygons = list(
                    map(
                        lambda x: writer.poly_to_linestr(
                            writer.poly_append_time(*x)
                        ),
                        [(T_1, P_1), (T_1, P_2), (T_1, P_3), (T_2, P_1)],
                    )
                )
                for poly_str, path in zip(polygons, paths):
                    db.exec(writer.exe_str, path, str(EXP), OBSERVER, poly_str)

    @classmethod
    def tearDownClass(cls):
        with common.DataBase.get_pg_db(settings) as db:
            db.conn.set_isolation_level(0)
            db.exec(f'DROP DATABASE {settings.POSTGRES_DB};')
            db.conn.set_isolation_level(1)
