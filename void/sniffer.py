#!/usr/bin/env python
"""
void_sniffer 0.2

Searches for FITS files without a custom header and outputs their paths.

Usage:
  void_sniffer SEARCH_DIR [--tmin=TIME_MIN] [--tmax=TIME_MAX] \
[--maxn=N] [--flag=HEADER | --noflag] [--verbosity=V]
  void_sniffer -v | --version
  void_sniffer -h | --help

Options:
  -i --tmin=TIME_MIN  Low time threshold
  -a --tmax=TIME_MAX  High time threshold
  -n --maxn=N         Stop after outputing N images
  -f --flag=HEADER    Name of the header to look for, [default: VISNJAN]
  -n --noflag         Skip header flag check
  -V --verbosity=V    Logging verbosity, 0 to 4 [default: 2]
  -h --help           Show this help screen
  -v --version        Show program name and version number
"""
# TODO versioning individual scripts?

import logging
import os
import sys
from typing import Optional

import docopt
from astropy.io import fits
from astropy.time import Time

from void import common

log = logging.getLogger(__name__)


class Sniffer:
    DISABLED_FLAG: str = '0'

    def __init__(
        self,
        search_dir: str,
        maxn: Optional[int] = None,
        tmin: Optional[str] = None,
        tmax: Optional[str] = None,
        flag_name: Optional[str] = None,
    ):
        self.search_dir = search_dir
        self.maxn = maxn
        self.tmin = tmin
        self.tmax = tmax
        if flag_name == self.DISABLED_FLAG:
            self.flag_name = None
        else:
            self.flag_name = flag_name
        self.count = 0
        self.time_first = None
        self.time_last = None

        if self.tmin:
            self.time_first = self.parse_time(self.tmin)
        if self.tmax:
            self.time_last = self.parse_time(self.tmax)
        log.debug('init done')

    def check_flag(self, fits_fname):
        log.debug('checking flag %s', fits_fname)
        with fits.open(fits_fname) as hdul:
            header_dict = hdul[0].header
            if header_dict.get(self.flag_name, '').strip():
                log.debug('true: %s', fits_fname)
                return True
        log.debug('false: %s', fits_fname)
        return False

    def find_fits(self):
        for root, _, files in os.walk(self.search_dir):
            for file in files:
                abs_fname = os.path.relpath(
                    os.path.normpath(os.path.join(root, file))
                )
                if self.validate_file(abs_fname):
                    yield abs_fname

    @staticmethod
    def parse_time(time_str):
        if 'T' not in time_str:
            time_str += 'T00:00:00.00'
        return Time(time_str, format='fits')

    def get_fits_time(self, fits_fname):
        with fits.open(fits_fname) as hdul:
            time_str = hdul[0].header['DATE-OBS']
            return self.parse_time(time_str)

    def flag_file(self, fits_fname):
        data, header = fits.getdata(fits_fname, header=True)
        header[self.flag_name] = 'True'
        fits.writeto(fits_fname, data, header, overwrite=True)

    def validate_file(self, fname):
        if not fname.endswith('.fits') and not fname.endswith('.fit'):
            return False
        if self.flag_name and self.check_flag(fname):
            return False
        if not self.filter_fits(fname):
            return False
        if self.maxn is not None and self.count >= self.maxn:
            raise StopIteration
        self.count += 1
        if self.flag_name:
            self.flag_file(fname)
        return True

    def filter_fits(self, fname_i):
        """
        Check if the string is a range or something else
        """
        time_fits = self.get_fits_time(fname_i)
        if self.time_first and time_fits < self.time_first:
            filter_value = False
        elif self.time_last and time_fits > self.time_last:
            filter_value = False
        else:
            filter_value = True
        log.debug(f'filter_value: {filter_value}')
        return filter_value


def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common.configure_log(arguments['--verbosity'])
    log.debug('initialising')
    sniffer = Sniffer(
        search_dir=arguments['SEARCH_DIR'],
        tmin=arguments['--tmin'],
        tmax=arguments['--tmax'],
        maxn=arguments['--maxn'],
        flag_name=arguments['--flag'],
    )
    for fname_i in sniffer.find_fits():
        sys.stdout.write(f'{fname_i}\n')


if __name__ == '__main__':
    main()
