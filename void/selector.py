#!/usr/bin/env python
"""
void_selector 0.1

Outputs paths of images from VOID which cross the ephemerides
 given by stdin.

Usage:
    void_selector --mpc [--log=LOG_FILE] [--verbosity=V]
    void_selector -r RA -d DE -t T -i DT [--log=LOG_FILE] [--verbosity=V]
    void_selector -v | --version
    void_selector -h | --help

Options:
  -m --mps            Accept ephemerides from MPC CP on stdin.
  -r --ra=RA          RA coordinate, in HMS format ("12h31m42s" or \
"12 31 42" or similar)
  -d --de=DE          DEC coordinate, in DMS format ("-10:03:44" or \
"-10 03 44" or similar)
  -t --time=TIME      Time of the exposure, in ISO format \
("2019-04-24T14:15:16")
  -i --interval=IVAL  Interval of time in which to search.
  -l --log=LOG_FILE   Path to log file. Otherwise uses stderr.
  -V --verbosity=V    Logging verbosity, 0 to 4 [default: 2]
  -h --help           Show this help screen
  -v --version        Show program name and version number

"""
import logging
import sys
import docopt
from astropy.coordinates import Angle
from astropy.time import Time

from void import common
from void.settings import settings
from void.common import DataBase
from void.writer import Writer

log = logging.getLogger(__name__)


class Selector:
    def __init__(self):
        settings.load()
        self.db = DataBase.get_void_db(settings)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def line_to_point(line_str):
        """ Extract RA, Dec and get timestamp from an ephemeris string. """
        line_spl = line_str[:39].split()
        year, month, date, hour, ra, dec = line_spl
        if len(hour) > 2:
            minutes = hour[2:]
        else:
            minutes = '00'
        hour = hour[:2]
        time_isot = (
            '-'.join([year, month, date])
            + 'T'
            + ':'.join([hour, minutes, '00.000'])
        )

        time_unix = parse_time(time_isot)
        ra = parse_degrees(ra)
        dec = parse_degrees(dec)

        return ra, dec, time_unix

    def linestr_points_intersection(self, line_points):
        """ Get all image paths from VOID crossing a linestring. """
        line_points.append(line_points[0])
        with Writer() as writer:
            line_str = writer.vert_to_linestr(line_points)
        exe_str = """
            SELECT observations.path FROM observations
            WHERE ST_3DIntersects(observations.poly,
            ST_GeomFromText(%s));
        """
        self.db.exec(exe_str, line_str)
        paths = self.db.cursor.fetchall()
        paths = [tup[0] for tup in paths]
        return paths

    def close(self):
        self.db.close()


def parse_degrees(degs):
    return float(Angle(degs, unit='degree').deg)


def parse_hours(hours):
    return float(Angle(hours, unit='hour').hour)


def parse_hours_to_deg(hours):
    return float(Angle(hours, unit='hour').degree)


def parse_time(time_isot):
    return Time(time_isot, format='isot', scale='utc').unix


def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common.configure_log(arguments['--verbosity'], arguments['--log'])
    log.debug('listening')

    selector = Selector()
    line_points = []

    try:
        if arguments['--mpc']:
            for line in sys.stdin:
                if not line:
                    continue
                ra, dec, time_unix = selector.line_to_point(line)
                line_points.append([ra, dec, time_unix])
                log.info(f'processing {line}')

        else:
            ra = parse_hours_to_deg(arguments['RA'])
            de = parse_degrees(arguments['DE'])
            tm = parse_time(arguments['T'])
            dt = parse_hours(arguments['DT']) * 3600
            t0 = tm - dt
            t1 = tm + dt
            line_points = [(ra, de, t0), (ra, de, t1)]

        paths = selector.linestr_points_intersection(line_points)
        for path in paths:
            sys.stdout.write(path + '\n')
    except KeyboardInterrupt:
        log.debug('SIGINT')


if __name__ == '__main__':  # pragma no cover
    main()
