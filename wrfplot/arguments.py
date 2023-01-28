#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Handle and validate user provided arguments """
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

    # Convert Linux's '~' to absolute path to make it workable
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
    """Validate if input file provided exist

    Args:
        path: Path to input file

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
        list: list of variable after omitting names not known to application
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
    """
    for method in cmap_methods:
        try:
            if getattr(cmaps, method):
                print(method)
        except AttributeError:
            pass
    """
