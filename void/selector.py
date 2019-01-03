#!/usr/bin/env python

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

