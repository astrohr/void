""" Usage: Reducer.py (FITS_FNAME) [--mark] """

import sys
from docopt import docopt
from astropy.io import fits
import logging
import json

import void.config as config

log = logging.getLogger(__name__)



def printHeaderData(fits_fname):
    """ 
    Prints header data from a certain FITS file as a JSON dictionary. 
    """

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

        x_ang_size = x_pix_size * x_binning * x_scale
        y_ang_size = y_pix_size * y_binning * y_scale

        return_dict = {
            'date-obs': date_obs, 
            'exposition': exp, 
            'focus': focus,
            'ra-center': ra_center, 
            'dec_center': dec_center,
            'x_ang_size': x_ang_size,
            'y_ang_size': y_ang_size
        }

        json_dict = json.dumps(return_dict)

        sys.stdout.write(f'{json_dict}\n')


def markReduced(fits_fname):

    log.info('Reducing: ', fits_fname)

    data, header = fits.getdata(fits_fname, header=True)

    header['REDUCED'] = 'True'

    fits.writeto(fits_fname, data, header, overwrite=True)



if __name__ == '__main__':

    arguments = docopt(__doc__)

    fits_fname = arguments['FITS_FNAME']
    mark = arguments['--mark']

    printHeaderData(fits_fname)

    if mark: 
        markReduced(fits_fname)