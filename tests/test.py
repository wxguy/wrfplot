#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module to test wrfplot application. """
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
import cartopy
import shutil
from pathlib import Path


def clean_cartopy_data_dir():
    """
    Clean the cartopy data directory before starting wrfplot.
    """
    if os.path.exists(cartopy_data_dir) and len(os.listdir(cartopy_data_dir)) > 0:
        print("Cartopy data directory is already populated with shapefile data. Cleaning now.")
        shutil.rmtree(cartopy_data_dir)
    else:
        print("Cartopy data directory is empty. Running wrfplot in clean mode.")

    return True


def plot_sfc_data(input_path, output_dir):
    """
    Plot surface variable data
    """
    cmd_options = [wrfplot_path, '--vars', 'slp,rh2,ppn,dummy', '--input', input_path, '--output', output_dir]
    if os.system('python ' + " ".join(cmd_options)) == 0:
        print('Successfully completed surface plots...')
        return True
    else:
        print('Failed to complete surface plots successfully...')
        return False
    

def plot_upper(input_path, output_dir):
    """
    Plot upper atmospheric data
    """
    cmd_options = [wrfplot_path, '--vars', 'u_winds,dummy,u_rh', '--input', input_path, '--output', output_dir]
    if os.system('python ' + " ".join(cmd_options)) == 0:
        print('Successfully completed upper atmospheric plots...')
        return True
    else:
        print('Failed to complete upper atmospheric plots successfully...')
        return False


def test(input_path, output_dir):
    cmd_options = [wrfplot_path, '--vars', 'u_winds,dummy,u_rh', '--ulevels', '900,450,dummy', '--input', input_path, '--output', output_dir]
    if os.system('python ' + " ".join(cmd_options)) == 0:
        print('Successfully completed upper atmospheric plots...')
        return True
    else:
        ('Failed to complete upper atmospheric plots successfully...')
        return False


def plot_animation(input_path, output_dir):
    cmd_options = [wrfplot_path, '--vars', 'T2,dummy,u_rh', '--gif', '--input', input_path, '--output', output_dir]
    if os.system('python ' + " ".join(cmd_options)) == 0:
        print('Successfully completed animation plot...')
        return True
    else:
        print('Failed to create animation plot...')
        return False


def plot_animation_with_speed(input_path, output_dir):
    cmd_options = [wrfplot_path, '--vars', 'T2,dummy', '--gif', '--gif-speed', '0.25'', --input', input_path, '--output', output_dir]
    if os.system('python ' + " ".join(cmd_options)) == 0:
        print('Successfully completed animation plot...')
        return True
    else:
        print('Failed to create animation plot...')
        return False


if __name__ == "__main__":
    home = str(Path.home())
    test_file_path = os.path.realpath(__file__)
    wrf_input_path = os.path.join(os.path.dirname(test_file_path), 'wrfout_data', 'wrfout_d01_2021-05-13_00_00_00')
    output_plot_dir = os.path.join(home, 'Documents', 'test_output_images')
    cartopy_data_dir = os.path.abspath(cartopy.config['data_dir'])
    wrfplot_path = os.path.join(os.path.dirname(test_file_path), '..', 'wrfplot', 'wrfplot.py')
    print('Utilising WRF model data from :', wrf_input_path)
    clean_cartopy_data_dir()
    plot_sfc_data(input_path=wrf_input_path, output_dir=output_plot_dir)
    plot_upper(input_path=wrf_input_path, output_dir=output_plot_dir)
    test(input_path=wrf_input_path, output_dir=output_plot_dir)
    plot_animation(input_path=wrf_input_path, output_dir=output_plot_dir)
    plot_animation_with_speed(input_path=wrf_input_path, output_dir=output_plot_dir)
    