import os
import unittest

from void import common
from void.settings import settings
from void.writer import Writer
from void.selector import Selector

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

    def test_line_to_point(self):
        line = (
            "2019 04 24 1430  "
            "09.0726    -06.407"
            "    105.5  20.5"
            "    3.90  345.4"
            "  303  +20   +36"
            "    0.72  133  -64   M"
        )
        expected = [9.0726, -6.407, 1_556_116_200]
        with Selector() as selector:
            output = list(selector.line_to_point(line))
            output[2] = round(output[2], 3)
        self.assertEqual(expected, output)

    def test_linestr_horiz(self):
        line_points = [[0, 0, T_1], [5, 0, T_1]]
        expected = ['P_1', 'P_2']
        with Selector() as selector:
            output = selector.linestr_points_intersection(line_points)
        self.assertEqual(expected, output)

    def test_linestr_horiz_disp(self):
        line_points = [[-1, 1.95, T_1], [6.98, -1.5, T_1]]
        expected = ['P_1', 'P_2']
        with Selector() as selector:
            output = selector.linestr_points_intersection(line_points)
        self.assertEqual(expected, output)

    def test_vert(self):
        line_points = [[0, 0, T_1], [0, 0, T_2]]
        expected = ['P_1', 'R_1']
        with Selector() as selector:
            output = selector.linestr_points_intersection(line_points)
        self.assertEqual(expected, output)

    def test_vert_disp(self):
        line_points = [[-1, -0.5, T_1], [1.58, 1.5, T_2]]
        expected = ['P_1', 'R_1']
        with Selector() as selector:
            output = selector.linestr_points_intersection(line_points)
        self.assertEqual(expected, output)

    def test_vert_angle(self):
        line_points = [[-1, -3, T_1], [1.58, 1.02, T_2]]
        expected = ['P_3', 'R_1']
        with Selector() as selector:
            output = selector.linestr_points_intersection(line_points)
        self.assertEqual(expected, output)
