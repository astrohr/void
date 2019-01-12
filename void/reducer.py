#!/usr/bin/env python
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
from astropy.io import fits

from void import common, config

log = logging.getLogger(__name__)


def read_header_data(fits_fname):
    """
    Read header data from a certain FITS file as a JSON dictionary.
    """
    log.debug('reading %s', fits_fname)

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

        log.debug('read %s', fits_fname)

        return {
            'date_obs': date_obs,
            'exposition': exp,
            'focus': focus,
            'ra_center': ra_center,
            'dec_center': dec_center,
            'x_deg_size': x_deg_size,
            'y_deg_size': y_deg_size,
        }


def encode_header_data(data):
    log.debug(f'JSON data: {data}')
    json_dict = json.dumps(data)
    return json_dict


def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common.configure_log(arguments['--verbosity'])
    log.debug('listening')

    try:
        for line in sys.stdin:
            fname = line.strip()
            if not fname:
                continue
            log.info(f'processing {fname}')
            try:
                data = read_header_data(fname)
                json_dict = encode_header_data(data)
                sys.stdout.write(f'{json_dict}\n')
            except FileNotFoundError:
                log.warning(f'FileNotFoundError: "{fname}"')
            except Exception as e:
                log.warning(f'{e}', exc_info=True)
        log.debug('EOF')
    except KeyboardInterrupt:
        log.debug('SIGINT')


if __name__ == '__main__':
    main()
