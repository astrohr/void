#!/usr/bin/env/ python
"""
void_reducer 0.1

Prints header data from a FITS filenames from stdin and optionally mark them.

Usage:
  void_reducer [--mark=MARK] [--verbosity=V]
  void_reducer -v | --version
  void_reducer -h | --help

Options:
  -m --mark=MARK      Mark the file
  -h --help           Show this help screen
  -v --version        Show program name and version number
  -V --verbosity=V    Logging verbosity, 0 to 4 [default: 2]
"""

import json
import logging
import sys

import docopt
from astropy.io import fits

from void import common, config, sniffer

log = logging.getLogger(__name__)


def print_header_data(fits_fname):
    """
    Prints header data from a certain FITS file as a JSON dictionary.
    """
    log.debug('printing data for %s', fits_fname)

    with fits.open(fits_fname) as hdul:
        header_dict = hdul[0].header

        date_obs = header_dict['DATE-OBS']
        exp = header_dict['EXPTIME']
        focus = header_dict['FOCUSPOS']
        ra_center = header_dict['OBJCTRA']
        dec_center = header_dict['OBJCTDEC']

        x_pix_size = header_dict['NAXIS1']
        y_pix_size = header_dict['NAXIS2']
        x_binning = header_dict['XBINNING']
        y_binning = header_dict['YBINNING']

        x_scale = config.SCALE_X_BIN1
        y_scale = config.SCALE_Y_BIN1

        x_deg_size = float(x_pix_size * x_binning * x_scale) / 3600
        y_deg_size = float(y_pix_size * y_binning * y_scale) / 3600

        return_dict = {
            'date_obs': date_obs,
            'exposition': exp,
            'focus': focus,
            'ra_center': ra_center,
            'dec_center': dec_center,
            'x_deg_size': x_deg_size,
            'y_deg_size': y_deg_size
        }

        json_dict = json.dumps(return_dict)
        sys.stdout.write(f'{json_dict}\n')


def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common.configure_log(arguments['--verbosity'])
    log.debug('initialising')

    mark = arguments['--mark']

    fnames_arr = []

    for line in sys.stdin:
        fnames_arr.append(line.strip())

    for fname in fnames_arr:
        print_header_data(fname)
        if mark:
            sniffer.Sniffer.flag_file(mark, fname)


if __name__ == '__main__':
    main()
