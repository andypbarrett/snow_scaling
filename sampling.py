'''Utilities to sample files'''

import numpy as np

from shapely.geometry import Polygon


def circle(x0=0, y0=0, radius=1000., npoints=360):
    '''Returns a Shapely Polygon for a circle

    :x0: x-coordinate of circle in meters
    :y0: y-coordinate of circle in meters
    :radius: radius of circle in meters
    '''

    x = [x0 + radius * np.cos(np.radians(theta))
         for theta in np.linspace(0., 359., npoints)]
    y = [y0 + radius * np.sin(np.radians(theta))
         for theta in np.linspace(0., 359., npoints)]

    return Polygon(list(zip(x, y)))

