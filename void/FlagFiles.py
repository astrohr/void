""" Flag all files in a certain directory as imaged in Visnjan. 
	
	Usage: FlagFiles.py (FLAG_DIR)
"""

from docopt import docopt
from astropy.io import fits

import Sniffer as snf

if __name__ == '__main__':

	arguments = docopt(__doc__)
	flag_dir = arguments['FLAG_DIR']

	fits_files = snf.findFits(flag_dir)

	print('Overwriting headers...')
	for fname_i in fits_files:

		print('Overwriting: ', fname_i)

		fits_absname = snf.absName(flag_dir, fname_i)

		data, header = fits.getdata(fits_absname, header=True)

		header['VISNJAN'] = 'True'

		fits.writeto(fits_absname, data, header, ovrewrite=True)

	print('Done!')