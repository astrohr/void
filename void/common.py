#!/usr/bin/env python
"""
Functions used in misc files.
"""


import logging
import docopt


LOG_FORMAT = (
    '%(levelname)-8s  %(asctime)s  %(process)-5d  %(name)-26s  %(message)s')


def configure_log(verbosity):
    levels = {
        '0': logging.CRITICAL,
        '1': logging.ERROR,
        '2': logging.WARNING,
        '3': logging.INFO,
        '4': logging.DEBUG,
    }
    if verbosity not in levels.keys():
        raise docopt.DocoptExit('--verbosity not one of 0, 1, 2, 3, 4')
    logging.basicConfig(level=levels[verbosity], format=LOG_FORMAT)
