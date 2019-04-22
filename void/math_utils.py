#!/usr/bin/env python
"""
Miscellaneous math functions
"""

import numpy as np  # noqa


def sort_ndarray(arr):
    return sorted(arr, key=sum)


def calculate_poly(image_center, image_x, image_y, pos_angle):
    """ Calculate coordinates of the image vertices. """

    image_center = np.asarray(image_center)
    pos_angle = np.deg2rad(360 - pos_angle)

    image_diag = np.sqrt(image_x ** 2 + image_y ** 2)
    phi = np.arctan2(image_y, image_x)

    poly_arr = []

    mult = 0.5 * image_diag
    m1_arr = [-1, -1, 1, 1]
    m2_arr = [1, -1, 1, -1]

    for i in range(4):
        m1, m2 = m1_arr[i], m2_arr[i]

        point_x = m1 * np.cos(pos_angle + m2 * phi)
        point_y = m1 * np.sin(pos_angle + m2 * phi)

        poly_arr.append([point_x, point_y])

    poly_arr = np.asarray(poly_arr)
    poly_arr *= mult
    poly_arr += image_center

    poly_arr = sort_ndarray(poly_arr)

    return poly_arr
