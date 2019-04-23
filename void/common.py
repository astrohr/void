#!/usr/bin/env python
"""
Functions used in misc files.
"""

import logging
import psycopg2

import docopt

LOG_FORMAT = (
    '%(levelname)-8s  %(asctime)s  %(process)-5d  %(name)-26s  %(message)s'
)


log = logging.getLogger(__name__)


def configure_log(verbosity):
    levels = {
        '0': logging.CRITICAL,
        '1': logging.ERROR,
        '2': logging.WARNING,
        '3': logging.INFO,
        '4': logging.DEBUG,
    }
    if verbosity not in levels.keys():
        raise docopt.DocoptExit('--verbosity not one of 0, 1, 2, 3, 4')
    logging.basicConfig(level=levels[verbosity], format=LOG_FORMAT)


class DataBase:
    def __init__(self, user, passwd, db_name, host, port):
        self.conn = psycopg2.connect(
            database=db_name, user=user, password=passwd, host=host, port=port
        )
        self.cursor = self.conn.cursor()
        log.debug('connection established')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False

    def exec(self, exe_str, *attr):
        self.cursor.execute(exe_str, attr)
        self.conn.commit()

    def close(self):
        self.cursor.close()

    @classmethod
    def get_pg_db(cls, settings):
        return cls(
            user=settings.POSTGRES_USER,
            passwd=settings.POSTGRES_PASSWORD,
            db_name='postgres',
            host='localhost',
            port='5433',
        )

    @classmethod
    def get_void_db(cls, settings):
        return cls(
            user=settings.POSTGRES_USER,
            passwd=settings.POSTGRES_PASSWORD,
            db_name=settings.POSTGRES_DB,
            host='localhost',
            port='5433',
        )
