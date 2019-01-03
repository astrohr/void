""" Usage: Reducer.py (FITS_FNAME) [--mark] """

from docopt import docopt
from astropy.io import fits
import logging

log = logging.getLogger(__name__)

def printHeaderData(fits_fname):

    with fits.open(fits_fname) as hdul:

        log.info('Printing header data for: ', fits_fname)

        header_dict = hdul[0].header

        date_obs = header_dict['DATE-OBS']
        exp = header_dict['EXPTIME']
        ra_center = header_dict['OBJCTRA']
        dec_center = header_dict['OBJCTDEC']
        focus = header_dict['FOCUSPOS']

        print(date_obs)
        print(exp)
        print(ra_center)
        print(dec_center)
        print(focus)


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