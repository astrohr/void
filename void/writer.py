#!/usr/bin/python
"""
void_writer 0.1

Inserts data from stdin into the VOID.

Usage:
    void_writer [--verbosity=V]
    void_writer -v | --version
    void_writer -h | --help

Options:
  -h --help           Show this help screen
  -v --version        Show program name and version number
  -V --verbosity=V    Logging verbosity, 0 to 4 [default: 2]

"""

import json
import logging
import sys

import docopt
import psycopg2
from astropy.time import Time

from void import common

log = logging.getLogger(__name__)


class Writer:
    def __init__(self):
        self.db_name = 'void'
        self.user = 'void'
        self.passwd = 'void'
        self.host = 'localhost'
        self.port = '5433'

        self.conn = psycopg2.connect(
            database=self.db_name,
            user=self.user,
            password=self.passwd,
            host=self.host,
            port=self.port,
        )

        self.cursor = self.conn.cursor()
        log.debug('connection established')

        self.create_table()
        log.debug('table created')

    def create_table(self):
        """
        Creates a table if one does not already exist in VOID.
        """
        self.cursor.execute('CREATE EXTENSION IF NOT EXISTS postgis;')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS observations '
            '(id SERIAL, '
            'path VARCHAR (500) NOT NULL, '
            'date_obs TIMESTAMP NOT NULL, '
            'exp FLOAT NOT NULL, '
            'observer VARCHAR (100), '
            'poly GEOMETRY(POLYGON) NOT NULL);'
        )
        return

    @staticmethod
    def decode_data(data_str):
        data_dict = json.loads(data_str)
        log.debug(f'data_dict: {data_dict}')
        return data_dict

    @staticmethod
    def poly_to_str(poly):
        poly_str = ','.join('{} {}'.format(*vert) for vert in poly)
        log.debug(f'poly_str: {poly_str}')
        return poly_str

    def insert_data(self, data_str):
        data_dict = self.decode_data(data_str)
        path, date, exp, observer, poly = data_dict.values()
        date_tstamp = Time(date, format='isot', scale='utc').unix
        poly_str = self.poly_to_str(poly)

        exe_str = """
            INSERT INTO observations (date_obs, path, exp, observer, poly) 
            VALUES ('{:s}', {}, {}, '{:s}', ST_MakePolygon(ST_GenFromText('LINESTRING({:s})'), 4326))
        """.format(
            path, date_tstamp, exp, observer, poly_str
        )

        self.cursor.execute(exe_str)
        return


def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common.configure_log(arguments['--verbosity'])
    log.debug('listening')

    writer = Writer()

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            log.info(f'processing {line}')
            try:
                writer.insert_data(line)
            except Exception as e:
                log.warning(f'{e}', exec_info=True)
        log.debug('EOF')
    except KeyboardInterrupt:
        log.debug('SIGINT')


if __name__ == '__main__':
    main()
