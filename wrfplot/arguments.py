#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Handle and validate user provided arguments """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation, either version 3 of the License, or any later version. 
 
wrfplot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with wrfplot. If not, 
see <http://www.gnu.org/licenses/>.
"""

__author__ = "J Sundar (wrf.guy@gmail.com)"

import os
import argparse
import configparser
import utils
import colormaps as cmaps


def dir_path(path):
    """Check if path provided is valid

    Args:
        path (str): Path to directory

    Results:
        str: if path is valid or else ArgumentTypeError
    """

    # Convert Linux's '~' to an absolute path to make it workable
    if path.startswith("~"):
        path = os.path.expanduser(path)
    previous_dir = os.path.dirname(path)
    # Either path to directory or one directory up should be available for saving images
    if os.path.isdir(path) or os.path.isdir(previous_dir):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"Input path provided '{path}' is not a valid directory..."
        )


def file_path(path):
    """Validate if an input file provided exists

    Args:
        path: Path to an input file

    Results:
        str: if path is valid or else ArgumentTypeError
    """

    if os.path.isfile(path):
        return path
    else:
        raise argparse.ArgumentTypeError(
            f"Input path provided '{path}' is not a valid file..."
        )


def validate_vars(input_vars):
    """Validate user provided input variables and return only variables that are supported by the application

    Args:
        input_vars (list): List of variables for plotting

    Results:
        list: list of variables after omitting names not known to application
    """

    final_vars = []
    non_supported = []
    config = configparser.ConfigParser()
    config.read(os.path.join(utils.data_dir(), "wrf_variables.ini"))
    # Check if input variable contain multiple paramters
    if "," not in input_vars:
        if input_vars in config.sections():
            return input_vars
        else:
            raise argparse.ArgumentTypeError(
                f"Input variable(s) provided '{input_vars}' is not valid..."
            )
    # Split the variables in to list and check for
    vars = input_vars.split(",")
    for var in vars:
        if var in config.sections():
            final_vars.append(var)
        else:
            non_supported.append(var)
    if not final_vars:
        raise argparse.ArgumentTypeError(
            f"Input variable(s) provided '{input_vars}' is not valid..."
        )
    if non_supported:
        print(
            f"ArugmentWarning: variable(s)",
            ",".join(non_supported),
            "are not supported. Skipping..",
        )

    return final_vars


def list_vars():
    """List supported variable names on terminal"""

    config = configparser.ConfigParser()
    config.read(os.path.join(utils.data_dir(), "wrf_variables.ini"))
    print("\n****    ****    ****    ****    ****    ****    ****")
    print(
        "Variables starting with 'u_' are upper air variable availabe at 925, 850, 700, 600, 500, 400, 300 and 200 hPa heights..."
    )
    print("****    ****    ****    ****    ****    ****    ****\n")
    for var in config.sections():
        print(
            "Variable " + utils.quote(var),
            "  --> " + config.get(var, "title") + " (" + config.get(var, "unit") + ")",
        )
    print("")


def list_cmaps():
    """Print list of available colormaps on terminal"""
    cmap_methods = dir(cmaps)
    print(cmap_methods)
    return cmap_methods


def validate_cmap(cmap):
    """Validate user colormap name

    Args:
        cmap (ste): Name of colormap

    Results:
        str: Name of colormap if supported
    """
    if not cmap in dir(cmaps):
        print("\nColormap", utils.quote(cmap), "is nor supported by wrfplot. Use '--list-cmaps' option to find list of supported colormaps.")
        return False
    else:
        print("\nUsing user provided colormap :", utils.quote(cmap))

        return cmap


def valid_range(ulevel):
    """ Validate input pressure level """
    if ulevel > 1000:
        print("Upper level" + utils.quote(str(ulevel)) + " can not be more than 1000")
        return False
    elif ulevel < 50:
        print("Upper level" + utils.quote(str(ulevel)) + " can not be less than 1000")
        return False
    else:
        return True

        
def validate_ulevels(ulevels):
    """Validate user provided upper atmospheric levels
    
    Args:
        ulevels (list): list of levels provided by user
    Results:
        list:   List of filtered levels. None is returned if nothing compatible with wrfplot
    """
    filtered_ulevels = []
    if ',' not in str(ulevels):
        if ulevels.isdigit():
            if valid_range(float(ulevels)) is True:
                filtered_ulevels.append(float(ulevels))
        elif isinstance(ulevels, str):
            print("Upper level can not have string in it. Omitting " + utils.quote(ulevels))
    else:
        for level in ulevels.split(','):
            if level.isdigit():
                if valid_range(float(level)) is True:
                    filtered_ulevels.append(float(level))
            elif isinstance(level, str):
                print("Upper level can not have string in it. Omitting " + utils.quote(level))

    if len(filtered_ulevels) > 0:
        output_str_lst = [str(x) for x in filtered_ulevels]
        print("\nUsing user provided upper level(s) : " + utils.quote(",".join(output_str_lst)))
        return filtered_ulevels
    else:
        print("\nNone of the levels are valid upper levels.")
        print("Defaulting to levels '925, 850, 700, 600, 500, 400, 300 & 200hPa' supported by wrfplot.")
        return None


def validate_clevels(clevels):
    """Validate user provided contour levels
    
    Args:
        ulevels (list or int): list or no of levels provided by user 
    Results:
        list or int:   List of filtered contour levels. False is returned if invalid levels are provided.
    """
    filtered_clevels = []
    if ',' not in clevels:
        if clevels.isdigit():
            if int(clevels) > 12:
                print("\nContour levels number must be kept maximum as 12. Defaulting to " , utils.quote("12"))
                return "12"
            else:
                print("\nUsing user provided upper clevel : " + utils.quote(clevels))
                return clevels
        elif isinstance(clevels, str):
            print("\nContour level can not have string in it. Omitting " + utils.quote(clevels))
            return False
    else:
        for level in clevels.split(','):
            if level.strip().isdigit():
                if int(level) in filtered_clevels:
                    print("\nContour level", level, "already exist. Not repeating it.")
                else:
                    filtered_clevels.append(int(level))
            elif isinstance(level, str):
                print("Contour levels can not have string in it. Omitting " + utils.quote(level))
    
    if len(filtered_clevels) == 0:
        print("Reverting to automatic contour levels supported by wrfplot.")
        return False
    else:
        output_str_lst = [str(x) for x in filtered_clevels]
        print("\nUsing user provided contour levels : " + utils.quote(",".join(sorted(output_str_lst))))
        return sorted(filtered_clevels)
                
            
def validate_gif_speed(seconds):
    """Validate user provided gif animation speed
    
    Args:
        seconds: Number of seconds to indicate gif speed
    Result:
        int: Number of seconds after validation or else 0.5
    """
    if seconds.replace('.', '').isdigit():
        print("\nUsing user provided gif speed:", utils.quote(seconds))
        return float(seconds)
    else:
        print("\nInvalid gif speed:", utils.quote(seconds))
        print("Defaulting to GIF animation speed to '0.5' seconds.")
        return 0.5
