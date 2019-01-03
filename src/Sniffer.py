""" Usage: Sniffer.py (SEARCH_DIR) [--time=SEARCH_STRING] [--maxn=MAXN] [--check] """

import os
from docopt import docopt
from astropy.time import Time
from astropy.io import fits
import logging

log = logging.getLogger(__name__)

def absName(search_dir, file):

	return os.path.abspath(os.path.join(search_dir, file))


def checkForFlag(fits_fname):

	with fits.open(fits_fname) as hdul:

		header_dict = hdul[0].header

		if 'VISNJAN' in header_dict and header_dict['VISNJAN'].strip() == 'True':
			return True

	print(fits_fname)
	return False


def findFits(search_dir, maxn=None, check=None):

	fits_fnames_arr = []

	log.info('Finding all FITS files...')

	for root, dirs, files in os.walk(search_dir):
		for file in files:
			if file.endswith('.fits') or file.endswith('.fit'):
				abs_fname = absName(search_dir, file)
				if check is not None:
					if checkForFlag(abs_fname) == True:
						fits_fnames_arr.append(abs_fname)

	fits_fnames_arr = sorted(fits_fnames_arr)

	if maxn is not None:
		fits_fnames_arr = fits_fnames_arr[:int(maxn)]

	return fits_fnames_arr


def timeStr2Object(time_str):

	if 'T' not in time_str:
		time_str += 'T00:00:00.00'

	astro_time_obj = Time(time_str, format='fits')

	return astro_time_obj


def getFitsTime(fits_fname):

	with fits.open(fits_fname) as hdul:
		
		time_str = hdul[0].header['DATE-OBS']
		time = timeStr2Object(time_str)

	return time

def getFitsRange(search_dir, range_str, maxn=None, check=None):

	fits_fnames = findFits(search_dir, check=check)
	filtered_fits_fnames = []

	log.info('Finding all FITS files within the given time range...')

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

	filtered_fits_fnames = sorted(filtered_fits_fnames)

	if maxn is not None:
		filtered_fits_fnames = filtered_fits_fnames[:int(maxn)]

	return filtered_fits_fnames


if __name__ == '__main__':

	arguments = docopt(__doc__)

	search_dir = arguments['SEARCH_DIR']
	search_string = arguments['--time']
	maxn = arguments['--maxn']
	check = arguments['--check']

	if search_string is None:

		fits_fnames = findFits(search_dir, maxn=maxn, check=check)

	else:

		fits_fnames = getFitsRange(search_dir, search_string, maxn=maxn, check=check)


	for fname_i in fits_fnames:
		print(fname_i)
