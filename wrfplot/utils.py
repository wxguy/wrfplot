#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module to deal with various operations repetadly used int he application  """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

wrfplot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with wrfplot. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "J Sundar (wrf.guy@gmail.com)"

import numpy as np
import matplotlib.pyplot as plt
import os
import socket
import colormaps as cmaps


def get_cmap(name):
    """Get colour map for a specific string name
    Args:
        name (str): Name of the colour map

    Returns:
        cmap: Maplotlib's cmap instance
    """

    if isinstance(name, list):
        return name
    try:
        cmap = getattr(cmaps, name)
    except AttributeError:
        cmap = cmaps.gui_default

    return cmap


# These are the list of projections supported by cartopy module
cartopy_proj = [
    "Mercator",
    "PlateCarree",
    "LambertConformal",
    "LambertCylindrical",
    "Miller",
    "Mollweide",
    "Orthographic",
    "Robinson",
    "Stereographic",
    "TransverseMercator",
    "InterruptedGoodeHomolosine",
    "RotatedPole",
    "OSGB",
    "EuroPP",
    "Geostationary",
    "Gnomonic",
    "NorthPolarStereo",
    "OSNI",
    "SouthPolarStereo",
]


def list_proj():
    # https://www.icsm.gov.au/education/fundamentals-mapping/projections/commonly-used-map-projections
    # https://pro.arcgis.com/en/pro-app/2.8/help/mapping/properties/plate-carree.htm
    print(
        "merc\t: 'Mercator'. Best Used in areas around the Equator and for marine navigation"
    )
    print(
        "pltcre\t: 'PlateCarree'. Used for simple portrayals of the world or regions with minimal geographic data and those not requiring accurate areas."
    )
    print(
        "lc: 'LambertConformal'. Best suitable for mid-latitudes e.g. USA, Europe and Australia"
    )
    print(
        "stc\t: 'Stereographic'. Best used in areas over the Poles or for small scale continental mapping"
    )

    return True


def quote(_str):
    """Quote a give string

    Args:
        _str (str): String which need to be quoted

    Returns:
        str: Quoted argument as string
    """

    return '"{}"'.format(_str)


def get_auto_resolution(data):
    """Find optimum multiplication factor to extract correct amount of data from numpy array

    Args:
        data (ndarray): Any numpy array

    Returns:
        integer: integer value that would be used for extracting ndarray data at particular intervals
    """

    fig = plt.gcf()
    size = fig.get_size_inches()  # size in pixels
    x_size = int(size[0])
    x_data = data.shape
    thin = int(x_data[0] / x_size) - 2

    return thin


def get_auto_range_calc(max, min, step):
    """Calculate range of data according to input data and not list

    Args:
        max: Max value of data
        min: Min value of data
        step:Steps in which data to be increased

    Returns:
        list: Range of data as list
    """

    x = int((max - min) / step)
    return x


def dir_to_list_files(path):
    """Function to return list of files for a given directory

    Args:
        path (str): Path to directory or file(s) or file

    Returns:
        list: List containing path to files
    """

    _in_files = []
    if os.path.isdir(path):
        _files = os.listdir(path)
        for _file in _files:
            _in_files.append(os.path.join(path, _file))
    else:
        _in_files = path.split(",")

    return _in_files


def get_auto_clevel(data, scale=12, slp=False):
    """Calculate automatic clevels from input data

    Args:
        data (ndarray): Input data in numpy format
        scale (int): The scale of the colour bar
        slp (bool): True to use Sea Level Pressure interval at 2hPa

    Returns:
        list: The c_level in list and in increasing form
    """

    c_levels = []
    max = data.max()
    min = data.min()
    if slp is True:
        for i in range(int(min), int(max), 1):
            if i % 2 == 0:
                if 950 <= i <= 1040:
                    c_levels.append(i)
    else:
        c_levels = np.linspace(min, max, scale)
        if not all(i < j for i, j in zip(c_levels, c_levels[1:])):
            return c_levels.sort()

    return c_levels


def c_level_ascending(c_level):
    """Make the contour level in ascending form

    Args:
        c_level (list): List containing values in assorted order

    Returns:
        list: List containing elements in ascending order
    """

    c_level = [float(i) for i in c_level]

    return all(x < y for x, y in zip(c_level, c_level[1:]))


def internet():
    """Check if internet exist on a host machine by pinging google domain

    Returns:
        bool: True if internet exist or else False
    """

    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass

    return False


def data_dir():
    """Get data directory

    Returns:
        str: Path to data directory
    """
    return os.path.join(os.path.dirname(__file__), "data")
