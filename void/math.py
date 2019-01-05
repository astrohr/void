#!/usr/bin/env python
"""
Miscallenaous math functions
"""

import numpy as np


def calculate_poly(image_center, image_x, image_y, pos_angle):
    """ Calculate image border points. """

    image_center = np.asarray(image_center)
    pos_angle = np.deg2rad(pos_angle)

    image_diag = np.sqrt(image_x ** 2 + image_y ** 2)
    gamma = np.arccos((image_x ** 2 + image_diag ** 2 -
                       image_y ** 2) / (2 * image_x * image_diag))
    delta = np.arccos((image_y ** 2 + image_diag ** 2 -
                       image_x ** 2) / (2 * image_y * image_diag))

    poly_arr = np.zeros(4)

    mult = 0.5 * image_diag
    m1, m2 = 1, -1
    f1, f2 = np.cos, np.sin
    add = gamma

    for i in range(4):
        if i > 2:
            m1, m2 = np.asarray([m1, m2]) * -1
            add = delta
        if i % 2 == 1:
            f1, f2 = f2, f1

        angle = pos_angle + add

        point_x = m1 * f1(angle)
        point_y = m2 * f2(angle)
        poly_arr[i] = [point_x, point_y]

    poly_arr *= mult
    poly_arr += image_center

    return poly_arr
