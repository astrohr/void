#!/usr/bin/env python
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
from astropy.time import Time

from void import common
from void.settings import settings
from void.common import DataBase

log = logging.getLogger(__name__)


class Writer:
    def __init__(self):
        settings.load()
        self.db = DataBase.get_void_db(settings)
        self.create_table()
        self.exe_str = """
            INSERT INTO observations (path, exp, observer, poly)
            VALUES (%s, %s, %s,
            ST_MakePolygon(ST_GeomFromText(%s)));
        """
        log.debug(f'exe_str: {self.exe_str}')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create_table(self):
        """ Creates a table if one does not already exist in VOID. """
        self.db.exec('CREATE EXTENSION IF NOT EXISTS postgis;')
        self.db.exec(
            'CREATE TABLE IF NOT EXISTS observations '
            '(id SERIAL, '
            'path VARCHAR (500) NOT NULL, '
            'exp FLOAT NOT NULL, '
            'observer VARCHAR (100), '
            'poly GEOMETRY(POLYGONZ) NOT NULL);'
        )
        log.debug('table created')

    @staticmethod
    def decode_data(data_str):
        data_dict = json.loads(data_str)
        log.debug(f'data_dict: {data_dict}')
        return data_dict

    @staticmethod
    def poly_append_time(date_tstamp, poly):
        """ Appends a timestamp to each polygon point and closes it. """
        poly.append(poly[0])
        poly = [[*poly[i], date_tstamp] for i in range(len(poly))]
        return poly

    @staticmethod
    def vert_to_linestr(poly):
        """ Converts an enclosed array of 3D points to a Linestring. """
        poly_str = ','.join('{} {} {}'.format(*vert) for vert in poly)
        log.debug(f'poly_str: {poly_str}')
        return "LINESTRING({:s})".format(poly_str)

    def insert_data(self, data_str):
        """ Inserts data from stdin into VOID. """
        data_dict = self.decode_data(data_str)
        path, date, exp, observer, poly = data_dict.values()
        date_tstamp = Time(date, format='isot', scale='utc').unix
        poly = self.poly_append_time(date_tstamp, poly)
        poly_str = self.vert_to_linestr(poly)
        self.db.exec(self.exe_str, path, str(exp), observer, poly_str)

    def close(self):
        self.db.close()


def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common.configure_log(arguments['--verbosity'])
    log.debug('listening')

    with Writer() as writer:
        try:
            for line in sys.stdin:
                line = line.strip()
                if not line:
                    continue
                log.info(f'processing {line}')
                try:
                    writer.insert_data(line)
                except Exception as e:
                    log.warning(f'{e}', exc_info=True)
            log.debug('EOF')
        except KeyboardInterrupt:
            log.debug('SIGINT')


if __name__ == '__main__':  # pragma no cover
    main()
