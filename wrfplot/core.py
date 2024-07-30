#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Core module to deal with wrf model output NetCDF files before plotting """
import sys

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
from tqdm import tqdm
import netCDF4 as nc
import numpy as np
import wrf
from wrf import getvar, get_cartopy, interplevel, latlon_coords, ALL_TIMES
from configparser import ConfigParser
import utils
import plot
import animation
import convert
from datetime import datetime
import warnings
import matplotlib
matplotlib.use("agg")
warnings.filterwarnings("ignore", module="matplotlib")
warnings.filterwarnings("ignore", module="datetime")


class WrfPlot:
    def __init__(
            self, input_path, output_path=None, variables=[], ulevels=None, dpi=150, cmap=False, animation=False,
            animation_speed=0.5, clevels=False,):
            self.nc_fh = None
            self.valid_input = None
            self.input = input_path
            self.output = output_path
            self.var = None
            self.var_data = None
            self.lats = None
            self.lons = None
            self.date_time = []
            self.ulevels = ulevels
            self.proj = None
            self.clevels = clevels
            self.cycle = None
            self.config = self.read_default_config()
            self.dpi = dpi
            self.cmap = cmap        
            self.animation = animation
            self.speed = animation_speed
            self.custom_title = None
            self.plot = plot.PlotMap(output_dir=output_path, dpi=dpi, clevels=clevels, config_file=self.config)
            self.total_vars = 1
            self.is_moving_domain = None
            self.pressure = None
            self.bar_update = 1

    def get_domain_state(self):
        if self.is_moving_domain is None:
            self.is_moving_domain = wrf.is_moving_domain(self.input)

    def read_default_config(self, path=""):
        config = ConfigParser()
        config.read(os.path.join(utils.data_dir(), "wrf_variables.ini"))
        wrf_defaults = {s: dict(config.items(s)) for s in config.sections()}
        # print(wrf_defaults['u_cape']['title'])
        return wrf_defaults

    def read_file(self, input_path):
        """Read input NetCDF file

        This function reads the input file provided and checks if it is a WRF model output

        Args:
            input_path (str): Path to input netcdf file

        Returns:
            bool: True if successful, False otherwise.
        """

        self.nc_fh = nc.Dataset(input_path, "r")
    
    def set_variable(self, variable):
        """ Set the name of variable to the object """
        self.var = variable
        if self.proj is None:
            self.proj = self.set_proj()

        self.cmap = self.set_cmap(var_name=variable)

    def to_datetime(self, dates):
        """Convert numpy datetime data into string time
        Args:
             dates (numpy): Numpy times variable containing numpy datetime format

        Returns:
            str: Datetime format in string
        """
        timestamp = (
            dates.values - np.datetime64("1970-01-01T00:00:00")
        ) / np.timedelta64(1, "s")

        return datetime.fromtimestamp(timestamp)

    def get_time_period(self):
        """Extract times of the WRF output file"""
        dates = getvar(self.nc_fh, 'Times', timeidx=ALL_TIMES)
        self.date_time = []
        for _date in dates:
            if not np.isnat(_date):
                date_time = self.to_datetime(_date)
                year = date_time.strftime("%Y")
                month = date_time.strftime("%m")
                day = date_time.strftime("%d")
                _time = date_time.strftime("%H:%M")
                self.date_time.append(day + "-" + month + "-" + year + "_" + _time)

        if len(self.date_time) > 0:
            self.cycle = self.date_time[0]

        return self.date_time

    def extract_data(self, var_name, u=None, v=None, idx_time=None, level=None):
        """Extract data for a given variable

        This function reads the data for a given variable through supported variables. Segregation of 2D and 3D data
        based on variable names is done here. If new variable names are to be added to application, then this function
        is required to be gone through thoroughly.

        Args:
            var (str): Name of the variable supported by the application

        Returns:
            Data, U component (default is None) and V component (default is None) in numpy array format
        """
        cape_2d = ["mcape", "mcin", "lcl", "lfc"]
        cloudfrac = ["low_cloudfrac", "mid_cloudfrac", "high_cloudfrac"]
        cape_3d = ["u_cape", "u_cin"]

        if var_name == "winds":
            u, v = getvar(self.nc_fh, "uvmet10", timeidx=idx_time, units='kt')
            var_data = getvar(self.nc_fh, "wspd_wdir10", timeidx=idx_time, units='kt')[0]
        elif var_name in cape_2d:
            var_data = getvar(self.nc_fh, "cape_2d", timeidx=idx_time)[cape_2d.index(var_name)]
        elif var_name in cloudfrac:
            var_data = getvar(self.nc_fh, "cloudfrac", timeidx=idx_time)[cloudfrac.index(var_name)]
        elif var_name in ['ppn', 'ppn_conv']:
            if var_name == 'ppn_conv':
                rain_c_current = getvar(self.nc_fh, "RAINC", timeidx=idx_time)
            else:
                rain_c_current = getvar(self.nc_fh, "RAINC", timeidx=idx_time)
                rain_nc_current = getvar(self.nc_fh, "RAINNC", timeidx=idx_time)
            if var_name == 'ppn_conv' and idx_time == 0:
                var_data = rain_c_current
            elif var_name == 'ppn' and idx_time == 0:
                var_data = rain_c_current + rain_nc_current

            if var_name == 'ppn_conv' and idx_time != 0:
                rain_c_previous = getvar(self.nc_fh, "RAINC", timeidx=(idx_time - 1))
                var_data = rain_c_current - rain_c_previous
            elif var_name == 'ppn' and idx_time !=0:
                rain_c_previous = getvar(self.nc_fh, "RAINC", timeidx=(idx_time-1))
                rain_nc_previous = getvar(self.nc_fh, "RAINNC", timeidx=(idx_time-1))
                var_data = (rain_c_current + rain_nc_current) - (rain_nc_previous + rain_c_previous)
        elif var_name == 'ppn_accum':
            var_data = (getvar(self.nc_fh, "RAINC", timeidx=idx_time) +
                        getvar(self.nc_fh, "RAINNC", timeidx=idx_time))
        elif 'u_' in var_name:
            var_data, u, v = self.interpolate_to(var_name=var_name, u_data=u, v_data=v, idx_time=idx_time, p_level=level)
        else:
            var_data = getvar(self.nc_fh, var_name, timeidx=idx_time)

        return self.convert_unit(var_data), u, v

    def interpolate_to(self, var_name, u_data=None, v_data=None, idx_time=None, p_level=None):
        """ Interpolate data to specific pressure height

        Receive data and interpolate to specific height level

        Args:
            var_name (str): Name of the variable supported by the application
            u_data (numpy array): U component wind
            v_data (numpy array): V component wind

        Returns:
            Data, U component (default is None) and V component (default is None) in numpy array format
        """
        pressure = getvar(self.nc_fh, "pressure", timeidx=idx_time)
        cape_3d = ["u_cape", "u_cin"]
        if var_name in cape_3d:
            var_data = getvar(self.nc_fh, "cape_3d", timeidx=idx_time)[cape_3d.index(var_name)]
        elif var_name == 'u_winds':
            u, v = getvar(self.nc_fh, "uvmet", timeidx=idx_time, units='kt')
            u_data = interplevel(u, pressure, p_level)
            v_data = interplevel(v, pressure, p_level)
            var_data = getvar(self.nc_fh, "wspd_wdir", timeidx=idx_time, units='kt')[0]
            # var_data_interp = interplevel(var_data, pressure, p_level)
        else:
            var_data = getvar(self.nc_fh, var_name.replace('u_', ''), timeidx=idx_time)

        var_data_interp = interplevel(var_data, pressure, p_level)

        return var_data_interp, u_data, v_data

    def plot_variable(self, var_name):
        """ Plotting surface and upper air variable """
        tqdm.write("\n*** Initialising plotting for variable : {_var} ***\n".format(_var=utils.quote(var_name)))
        if self.var is None:
            self.set_variable(variable=var_name)
        if self.ulevels is None:
            self.ulevels = [925, 850, 700, 600, 500, 400, 300, 200]
        if "u_" not in self.var:
            img_paths = []
            with tqdm(total=(self.total_vars * len(self.get_time_period())), desc="Completed", leave=False, position=0,
                      colour="green") as pbar:
                for index, _date_time in enumerate(self.get_time_period()):
                    tqdm.write(f"\tPlotting {utils.quote(var_name)} for Time : {utils.quote(_date_time)} UTC")
                    img_path = self.make_map(var_name=var_name, idx_time=index, time_fcst=_date_time)
                    self.bar_update = self.bar_update + 1
                    pbar.update(self.bar_update - pbar.n)
                    if img_path is not None:
                        img_paths.append(img_path)

                if self.animation is not False:
                    self.make_animation(var_name=var_name, img_paths=img_paths)
                self.reset_axes()

        elif "u_" in self.var:
            img_paths_p_level = []
            with tqdm(total=len(self.total_vars * self.ulevels * len(self.get_time_period())),
                      desc="Completed", leave=False, position=0, colour="green") as pb_level:
                for ulevel in self.ulevels:
                    for index, time_fcst in enumerate(self.date_time):
                        tqdm.write(f"\tPlotting {utils.quote(var_name)} for level {utils.quote(ulevel)} hPa and Time :"
                                   f" {utils.quote(time_fcst)} UTC")
                        img_path = self.make_map(var_name=var_name, idx_time=index, time_fcst=time_fcst, p_level=ulevel)
                        self.bar_update = self.bar_update + 1
                        pb_level.update(self.bar_update - pb_level.n)
                        if img_path is not None:
                            img_paths_p_level.append(img_path)
                        # pb_level.update()

                    if self.animation is not False:
                        self.make_animation(var_name=var_name, img_paths=img_paths_p_level)

                self.reset_axes()

    def reset_axes(self):
        """ Reset figure axes to make it ready for next iteration of plots
        """
        self.cmap = False
        self.clevels = False
        self.plot.cbar = False
        self.plot.c_bar_extend = None

    def make_animation(self, var_name, img_paths):
        """ Make animation for given image paths
        """
        if len(img_paths) > 0:
            output_gif_name = os.path.join(os.path.dirname(img_paths[0]), var_name + '-' +
                                           self.date_time[0].replace(":", "_")) + '.gif'
            animation.make_animation(img_paths, output_gif_name, speed=self.speed)
        else:
            tqdm.write(f"\nNot enough images available to make GIF image for variable {utils.quote(var_name)}...\n")

    def make_map(self, var_name, idx_time=None, time_fcst=None, p_level=None):
        """ Make a map for a given variable
        """
        data, u_data, v_data = self.extract_data(var_name, idx_time=idx_time, level=p_level)
        lats, lons = latlon_coords(data)
        # clevels = self.set_clevels(var_name=var_name, var_data=data)
        if self.config[var_name]["clevels"] == 'auto':
            clevels = utils.get_auto_clevel(data=data)
        else:
            clevels = self.set_clevels(var_name=var_name, var_data=data)
        if var_name == 'slp':
            img_path = self.plot.contour(var_name=var_name, lons=lons, lats=lats, data=data, clevels=clevels,
                                         title=self.get_title(var_name, time_fcst), colors='blue', fcst_time=time_fcst)
        elif var_name in ['winds', 'u_winds']:
            img_path = self.plot.winds(var_name=var_name, lons=lons, lats=lats, u_data=u_data, v_data=v_data,
                                       wspd=data, title=self.get_title(var_name, time_fcst, p_level), level=p_level,
                                       clevels=clevels, colors='black', cmap=self.cmap, fcst_time=time_fcst)
        else:
            img_path = self.plot.contour_fill(var_name=var_name, lons=lons, lats=lats, data=data, clevels=clevels,
                                              cmap=self.cmap, colors='black', title=self.get_title(var_name, time_fcst, p_level ),
                                              fcst_time=time_fcst, level=p_level)

        return img_path

    def set_cmap(self, var_name):
        """Get cmap from variable.ini file"""
        if self.cmap is False:
            cmap_name = self.config[var_name]["cmap"]
        else:
            cmap_name = self.cmap

        return utils.get_cmap(cmap_name)

    def extract_lats_lons(self, var_data):
        """Extract lat & lon data and update ``self.lats`` and ``self.lons`` variables accordingly"""
        lats, lons = latlon_coords(var_data)
        if lats.ndim == 3:
            self.lats = lats[0]
            self.lons = lons[0]
        else:
            self.lats = lats
            self.lons = lons

    def set_proj(self):
        """Get projection details from data extracted"""
        data = getvar(self.nc_fh, 'T2')
        if self.proj is None:
            if data.ndim == 3:
                self.proj = get_cartopy(data[0])
            elif data.ndim == 4:
                self.proj = get_cartopy(data[0, 0])
            else:
                self.proj = get_cartopy(data)
        return self.proj
    
    def get_title(self, var_name, time_fcst, level=None):
        """Get title from a config file"""
        if self.custom_title is not None:
            return self.custom_title
        else:
            if level is None:
                return self.config[var_name]["title"] + " (" + self.config[var_name]["unit"] + ")\n" \
                             "Cycle : " + self.cycle + " UTC  |  Validity : " + time_fcst  + " UTC"
            else:
                return self.config[var_name]["title"] + " (" + self.config[var_name]["unit"] + ") at " \
                           + str(int(level)) + " hPa\nCycle : " + self.cycle + " UTC  |  Validity : " + time_fcst + " UTC"

    def set_clevels(self, var_name, var_data):
        """ Create automatic contour levels for specific variable"""
        if self.var == "slp":
            self.clevels = utils.get_auto_clevel(var_data, slp=True)
        else:
            self.clevels = utils.get_clevels(var_name=var_name, clevels=self.clevels, data=var_data)

        return self.clevels

    def convert_unit(self, data):
        """Convert data to another unit"""
        if self.var in ["T2", "u_temp", "u_theta", "u_tv", "u_twb", "u_temp"]:
            return convert.k_to_c(data)
        elif self.var in ["low_cloudfrac", "mid_cloudfrac", "high_cloudfrac"]:
            return np.round(data * 100)
        else:
            return data
