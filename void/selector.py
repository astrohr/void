#!/usr/bin/env python
""" 
void_selector 0.1

Finds images in a given directory which contain a given point or polygon.

Usage:
  void_selector SEARCH_DIR [--point=POINT | --poly_pts=POLY_PTS] \
[--verbosity=V]
  void_selector -v | --version
  void_selector -h | --help

Options:
  -p --point          Point which is checked
  -l --poly_pts       List containing the polygon points which are checked
  -v --version        Show program name and version number
  -V --verbosity=V    Logging verbosity, 0 to 4 [default: 2]
"""


def point_within_area(point, area_ll, area_ur):
    ra_p, dec_p = point
    ra_ll, dec_ll = area_ll
    ra_ur, dec_ur = area_ur
    if ra_ll < ra_p < ra_ur and dec_ll < dec_p < dec_ur:
        return True
    return False


def poly_within_area(poly_points, area_ll, area_ur):
    for point in poly_points:
        if not point_within_area(point, area_ll, area_ur):
            return False
    return True
