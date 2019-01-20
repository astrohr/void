#!/usr/bin/env/ python
"""
void_reducer 0.1

Prints header data from a FITS filenames from stdin.

Usage:
  void_reducer [--verbosity=V]
  void_reducer -v | --version
  void_reducer -h | --help

Options:
  -h --help           Show this help screen
  -v --version        Show program name and version number
  -V --verbosity=V    Logging verbosity, 0 to 4 [default: 2]
"""

import json
import logging
import sys

import docopt
import numpy as np
from astropy.io import fits

from void import common

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
        ra_center = header_dict['CRVAL1']
        dec_center = header_dict['CRVAL2']

        x_pix_size = header_dict['NAXIS1']
        y_pix_size = header_dict['NAXIS2']

        # Scaling factors in [deg/px]
        x_scale = abs(header_dict['CDELT1'])
        y_scale = abs(header_dict['CDELT2'])

        x_deg_size = float(x_pix_size * x_scale)
        y_deg_size = float(y_pix_size * y_scale)

        pos_angle = header_dict['PA']

        # Limiting magnitude
        mag_norm = header_dict['starZMAG']
        mag_abs = mag_norm + 2.5 * np.log(exp)

        return_dict = {
            'date_obs': date_obs,
            'exposition': exp,
            'focus': focus,
            'ra_center': ra_center,
            'dec_center': dec_center,
            'x_deg_size': x_deg_size,
            'y_deg_size': y_deg_size,
            'pos_angle': pos_angle,
            'abs_magnitude': mag_abs
        }

        json_dict = json.dumps(return_dict)
        sys.stdout.write(f'{json_dict}\n')


def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common.configure_log(arguments['--verbosity'])
    log.debug('initialising')

    fnames_arr = []

    for line in sys.stdin:
        fnames_arr.append(line.strip())

    for fname in fnames_arr:
        print_header_data(fname)


if __name__ == '__main__':
    main()
