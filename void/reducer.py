#!/usr/bin/env/ python
""" 
void_reducer 0.1

Prints header data from a FITS file and optionally marks it as 'reduced'. 

Usage: 
  void_reducer FITS_FNAME [--mark] [--verbosity=V]
  void_reducer -v | --version
  void_reducer -h | --help

Options:
  -m --mark           Mark the file as reduced
  -h --help           Show this help screen
  -v --version        Show program name and version number
  -V --verbosity=V    Logging verbosity, 0 to 4 [default: 2]
"""

import sys
import docopt
from astropy.io import fits
import logging
import json

import void.common as common
import void.config as config

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
            'date-obs': date_obs, 
            'exposition': exp, 
            'focus': focus,
            'ra-center': ra_center, 
            'dec_center': dec_center,
            'x_deg_size': x_deg_size,
            'y_deg_size': y_deg_size
        }

        json_dict = json.dumps(return_dict)
        sys.stdout.write(f'{json_dict}\n')

def mark_reduced(fits_fname):

    log.debug('reducing %s', fits_fname)
    data, header = fits.getdata(fits_fname, header=True)
    header['REDUCED'] = 'True'
    fits.writeto(fits_fname, data, header, overwrite=True)

def main():
    name_and_version = __doc__.strip().splitlines()[0]
    arguments = docopt.docopt(__doc__, help=True, version=name_and_version)
    common._configure_log(arguments['--verbosity'])
    log.debug('initialising')

    fits_fname = arguments['FITS_FNAME']
    mark = arguments['--mark']

    print_header_data(fits_fname)
    if mark: 
        mark_reduced(fits_fname)


if __name__ == '__main__':
    main()