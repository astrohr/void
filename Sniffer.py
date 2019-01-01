""" Usage: sniffer.py (SEARCH_DIR) [--newer_than=TIMESTAMP] [--max_batch_size=MAXN]
"""

import os
from docopt import docopt
from astropy.io import fits

def findFits(search_dir):

	fits_fnames_arr = []

	for root, dirs, files in os.walk(search_dir):
		for file in files:
			if file.endswith('.fits') or file.endswith('.fit'):
				abs_fname = os.path.abspath(os.path.join(search_dir, file))
				fits_fnames_arr.append(abs_fname)

	return fits_fnames_arr

def getFitsTime(fits_fname):

	hdul = fits.open(fits_fname)

	time = hdul[0].header['DATE-OBS']

	hdul.close()

	return time

if __name__ == '__main__':

	arguments = docopt(__doc__)

	print(arguments)

	search_dir = arguments['SEARCH_DIR']
	timestamp = arguments['--newer_than']
	maxn = arguments['--max_batch_size']

	fits_fnames = findFits(search_dir)

	for fname_i in fits_fnames:

		print(fname_i, getFitsTime(fname_i))