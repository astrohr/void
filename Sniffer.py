""" Usage: sniffer.py (SEARCH_DIR) [--newer_than=TIMESTAMP] [--max_batch_size=MAXN]
"""

import os
from docopt import docopt
from astropy.time import Time
from astropy.io import fits

def findFits(search_dir):

	fits_fnames_arr = []

	for root, dirs, files in os.walk(search_dir):
		for file in files:
			if file.endswith('.fits') or file.endswith('.fit'):
				abs_fname = os.path.abspath(os.path.join(search_dir, file))
				fits_fnames_arr.append(abs_fname)

	return fits_fnames_arr


def timeStr2Object(time_str):

	if 'T' not in time_str:
		time_str += 'T00:00:00.00'

	astro_time_obj = Time(time_str, format='fits')

	return astro_time_obj


def getFitsTime(fits_fname):

	hdul = fits.open(fits_fname)

	time_str = hdul[0].header['DATE-OBS']

	time = timeStr2Object(time_str)

	hdul.close()

	return time


def getFitsRange(range_str, search_dir):

	fits_fnames = findFits(search_dir)
	filtered_fits_fnames = []

	# Check if the string is a range or something else
	if ',' in range_str:

		before_comma, after_comma = range_str.split(',')

		time_first = timeStr2Object(before_comma[1:]) 
		time_last = timeStr2Object(after_comma[1:-1])

		for fname_i in fits_fnames:
			time_fits = getFitsTime(fname_i)
			if time_first < time_fits < time_last:
				filtered_fits_fnames.append(fname_i)

	else:
		sign = range_str[0]
		time_thresh = timeStr2Object(range_str[2:])

		if sign == '>':
			for fname_i in fits_fnames:
				time_fits = getFitsTime(fname_i)
				if time_fits > time_thresh:
					filtered_fits_fnames.append(fname_i)

		elif sign == '<':
			for fname_i in fits_fnames:
				time_fits = getFitsTime(fname_i)
				if time_fits < time_thresh:
					filtered_fits_fnames.append(fname_i)

	return filtered_fits_fnames


if __name__ == '__main__':

	arguments = docopt(__doc__)

	print(arguments)

	search_dir = arguments['SEARCH_DIR']
	timestamp = arguments['--newer_than']
	maxn = arguments['--max_batch_size']

	fits_fnames = findFits(search_dir)

	for fname_i in fits_fnames:

		print(fname_i, getFitsTime(fname_i))