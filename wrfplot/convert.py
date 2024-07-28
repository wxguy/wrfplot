#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module to convert data from commonly used unit to another """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation, either version 3 of the License, or any later version. 
 
wrfplot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with wrfplot. If not, 
see <http://www.gnu.org/licenses/>.
"""

import numpy as np


def wind_spddir_to_uv(wspd, wdir):
    """calculated the u and v wind components from wind speed and direction

    Args:
        wspd (ndarray): wind speed
        wdir (ndarray): wind direction

    Results:
        u (ndarray): u wind component
        v (ndarray): v wind component
    """

    rad = 4.0 * np.arctan(1) / 180.0
    u = -wspd * np.sin(rad * wdir)
    v = -wspd * np.cos(rad * wdir)

    return u, v


def wind_uv_to_dir(U, V):
    """Calculates the wind direction from the u and v component of wind.

    Takes into account the wind direction coordinates is different than the
    trig unit circle coordinate. If the wind direction is 360 then returns zero
    (by %360)

    Args:
      U (ndarray): west/east direction (wind from the west is positive, from the east is negative)
      V (ndarray): south/noth direction (wind from the south is positive, from the north is negative)

    Results:
        float: Wind direction from 0-360
    """

    WDIR = (270 - np.rad2deg(np.arctan2(V, U))) % 360
    return WDIR


def wind_uv_to_spd(U, V):
    """
    Calculates the wind speed from the u and v wind components

    Args:
      U (ndarray): west/east direction (wind from the west is positive, from the east is negative)
      V (ndarray): south/noth direction (wind from the south is positive, from the north is negative)

    Results:
        float: Wind speed
    """

    # WSPD = np.sqrt(np.square(U) + np.square(V))
    WSPD = np.power(np.power(U, 2) + np.power(V, 2), 0.5)
    return WSPD


def pa_to_hpa(pres):
    """Convert pa to hPa

    Args:
        pres (ndarray): Pressure in (Pa)

    Returns:
        ndarrary: Pressure in (hPa)
    """

    pres_hpa = pres * 0.01
    return pres_hpa


def k_to_c(tempk):
    """Convert kelvin to celcius

    Args:
        tempk (ndarray): Temp in deg (K)

    Returns:
        ndarrary: Temp in in (C)
    """

    tempc = tempk - 273.15
    return tempc


def k_to_f(tempk):
    """Convert kelvin to fahreinheit

    Args:
        tempk (ndarray): Temp in deg (K)

    Returns:
        ndarrary: Temp in (F)
    """

    tempc = k_to_c(tempk)
    tempf = tempc * (9.0 / 5.0) + 32.0
    return tempf


def c_to_f(tempc):
    """Convert deg Cencius to Fahreinheit

    Args:
        tempc (ndarray): Temp in deg (C)

    Returns:
        ndarrary: Temp in (F)
    """

    tempf = tempc * (9.0 / 5.0) + 32.0
    return tempf


def ms_to_kts(spd):
    """Convert ms^-1 to Kts

    Args:
        spd (ndarray): Speed in (ms^-1)

    Returns:
        ndarrary: Speed in (knots)
    """

    spdkts = spd * 1.94384449
    return spdkts


def mm_to_in(ppn):
    """Convert mm to inch

    Args:
        ppn (ndarray): Precipitation in (mm)

    Returns:
        ndarrary: Precipitation in (inches)
    """

    ppnin = ppn * 0.0393701
    return ppnin


def theta_to_temp(theta, totalp):
    """Convert data from theta to temperature

    Args:
        theta (ndarray): Potential temperature (K)
        totalp (ndarray): Total Pressure (Pa)

    Returns:
        ndarrary: Temperature (K)
    """

    tempsfac = ((totalp * 0.01) / 1000.0) ** (
        8.314462618 / 1004.0
    )  # factor to multiply theta by
    temps = theta * tempsfac
    return temps
