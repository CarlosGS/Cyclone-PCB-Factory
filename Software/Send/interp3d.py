#!/usr/bin/env python
"""
Title: interp3d.py - interpolate to a set of points in 3-dimensional space
Author: Craig Arthur, craig.arthur@ga.gov.au
CreationDate: 2012-08-22
Description: Use scipy.ndimage.interpolation.map-coordinates to interpolate
             data in three dimensions.

Version: $Rev$
Id: $Id$
"""

import numpy
import pdb
from scipy.ndimage.interpolation import map_coordinates

def interp3d(input_array, coords, 
             scale=[360., 180., 365.],
             offset=[0.,-90.,0.]):
    """
    Wrapper to scipy.ndimage.interpolation.map_coordinates, which
    converts coordinates of points to indices that correspond to the
    array.  We assume that one is working with lon, lat, day data
    (i.e. initially designed to work with daily long term mean sea
    level pressure)

    Input:
    input_array - a 3-d array of data at regular intervals, representing the 
                  data to be evaluated
    coords - a 3xn array of coordinates at which the data in input_array
             will be interpolated
    scale - a scale factor that reduces the coords values to the range of
            indices in input_array
    offset - an offset factor that is subtracted from the coords values
             before adjusting the scale (above)

    Output:
    1-d array of values corresponding to the interpolated values 
    at the points given in 'coords'

    Example: vals = interp3d( data, coords, 
                              scale=[360., 180., 365.],
                              offset=[0.,-90.,0.] )

    """

    if input_array.ndim != 3:
        raise ValueError('Input array has incorrect shape')
    if coords.shape[0] != 3:
        raise ValueError('Coordinates of points must be 3-d')

    dims = input_array.shape
    indices = [d*(c - o) / s for d,c,o,s in 
               zip(dims,coords,offset,scale)]

    values = map_coordinates(input_array,indices, mode='wrap')

    return values

