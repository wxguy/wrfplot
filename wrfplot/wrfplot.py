#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Module to deal with wrf model output NetCDF files """
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
import traceback

# Set these env variables to avoid font related errors
os.environ["FONTCONFIG_PATH"] = "$CONDA_PREFIX/etc/fonts/"
os.environ["FONTCONFIG_FILE"] = "$CONDA_PREFIX/etc/fonts/fonts.conf"
# Have to set update env variables before importing pyproj module when running from freeze mode
custom_pyproj_dbase_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "pyproj", "proj"
)
if os.path.exists(custom_pyproj_dbase_dir):
    os.environ["PROJ_LIB"] = custom_pyproj_dbase_dir
    os.environ["PATH"] += os.pathsep + custom_pyproj_dbase_dir
    os.environ["PATH"] += os.path.dirname(os.path.abspath(__file__))

import platform
import sys
import argparse
from tqdm import tqdm
import netCDF4 as nc
import numpy as np
import arguments
from datetime import datetime
from wrf import getvar, smooth2d, get_cartopy, interplevel, latlon_coords, ALL_TIMES
import json
from configparser import ConfigParser
import fileio
import utils
import plot
import convert
from _version import __version__
import warnings
import matplotlib

matplotlib.use("agg")
warnings.filterwarnings("ignore", module="matplotlib")
warnings.filterwarnings("ignore", module="datetime")


class Wrfplot(object):
    """Main class to deal with WRF input data"""

    def __init__(
        self, input_path, output_path=None, variables=[], ulevels=None, dpi=150
    ):
        self.input_file = input_path
        self.nc_fh = None
        self.valid_input = None
        self.output = output_path
        self.vars = variables
        self.var = None
        self.var_data = None
        self.lats = None
        self.lons = None
        self.date_time = []
        self.ulevels = ulevels
        self.ulevel = None
        self.proj = None
        self.clevels = []
        self.cycle = None
        self.file = fileio.FileIO(self.input_file)
        self.config = ConfigParser()
        self.config.read(os.path.join(utils.data_dir(), "wrf_variables.ini"))
        self.dpi = dpi
        self.U = None
        self.V = None
        self.rainc = None
        self.rainnc = None

    def read_file(self, input_path):
        """Read input NetCDF file

        This function reads the input file provided and checks if it is a WRF model output

        Args:
            input_path (str): Path to input netcdf file

        Returns:
            bool: True if successful, False otherwise.
        """

        if self.file.is_wrf():
            self.nc_fh = nc.Dataset(input_path, "r")
            return self.nc_fh
        else:
            return False

    def read_data(self, var):
        """Extract data for a given variable

        This function reads the data for a given variable through supported variables. Segregation of 2D and 3D data
        based on variable names are done here. If new variable names are to be added to application, then this function
        is required to be gone through thoroughly.

        Args:
            var (str): Name of the variable supported by the application

        Returns:
            None
        """
        self.var = var
        if "u_" in var:
            var = var.replace("u_", "")
        cape_2d = ["mcape", "mcin", "lcl", "lfc"]
        cloudfrac = ["low_cloudfrac", "mid_cloudfrac", "high_cloudfrac"]
        cape_3d = ["u_cape", "u_cin"]
        # cape_2d variable contain few other variables within. Extract cape_2d first to unpack the rest
        if self.var in cape_2d:
            self.var_data = getvar(self.nc_fh, "cape_2d", ALL_TIMES)[
                cape_2d.index(self.var)
            ]
        elif self.var in cloudfrac:
            self.var_data = getvar(self.nc_fh, "cloudfrac", ALL_TIMES)[
                cloudfrac.index(self.var)
            ]
        elif self.var in cape_3d:
            self.var_data = getvar(self.nc_fh, "cape_3d", ALL_TIMES)[
                cape_3d.index(self.var)
            ]
        elif self.var in ["winds", "u_winds"]:
            if self.var == "winds":
                uvmet10 = self.U = getvar(self.nc_fh, "uvmet10", ALL_TIMES, units="kt")
                self.U = uvmet10[0]
                self.V = uvmet10[1]
                # self.U = getvar(self.nc_fh, 'U10', ALL_TIMES) * 1.94384449
                # self.V = getvar(self.nc_fh, 'V10', ALL_TIMES) * 1.94384449
                self.var_data = getvar(self.nc_fh, "wspd_wdir10", ALL_TIMES)[0]
            else:
                uvmet = self.U = getvar(self.nc_fh, "uvmet", ALL_TIMES, units="kt")
                self.U = uvmet[0]
                self.V = uvmet[1]
                # self.U = getvar(self.nc_fh, 'U10', ALL_TIMES) * 1.94384449
                # self.V = getvar(self.nc_fh, 'V10', ALL_TIMES) * 1.94384449
                self.var_data = getvar(self.nc_fh, "wspd_wdir", ALL_TIMES)[0]
        elif self.var == "ppn_accum":
            # netCDF data not extracted using diagnostic variables will not have cartopy instance.
            # So extract dummy variable to get cartopy first. The same goes to 'ppn_conv' and 'ppn' variables.
            self.proj = get_cartopy(getvar(self.nc_fh, "T2"))
            self.var_data = getvar(self.nc_fh, "RAINC", ALL_TIMES) + getvar(
                self.nc_fh, "RAINNC", ALL_TIMES
            )
        elif self.var == "ppn":
            self.proj = get_cartopy(getvar(self.nc_fh, "T2"))
            self.rainc = getvar(self.nc_fh, "RAINC", ALL_TIMES)
            self.rainnc = getvar(self.nc_fh, "RAINNC", ALL_TIMES)
            self.var_data = self.rainc
        elif self.var == "ppn_conv":
            self.proj = get_cartopy(getvar(self.nc_fh, "T2"))
            self.var_data = getvar(self.nc_fh, "RAINC", ALL_TIMES)
        else:
            self.var_data = getvar(self.nc_fh, var, ALL_TIMES)

    def read_latlons(self):
        """Extract lat & lon data and update ``self.lats`` and ``self.lons`` instance variables accordingly"""
        self.lats, self.lons = latlon_coords(self.var_data)

    def plot_variables(self):
        """A wrapper function to redirect plotting to surface and upper air variables to respective function"""
        self.get_proj()
        self.get_time_period()
        if self.ulevels is None:
            self.ulevels = [925, 850, 700, 600, 500, 400, 300, 200]
        if "u_" not in self.var:
            self.plot_sfc()
        elif "u_" in self.var:
            self.plot_upper()

        return True

    def to_datetime(self, date):
        """Convert numpy datetime data into string time
        Args:
             date(numpy): Numpy times variable containing numpy datetime format

        Returns:
            str: Datetime format in string
        """
        timestamp = (
            date.Time.values - np.datetime64("1970-01-01T00:00:00")
        ) / np.timedelta64(1, "s")

        return datetime.utcfromtimestamp(timestamp)

    def get_time_period(self):
        """Extract times of the WRF output file"""
        dates = self.var_data.Time
        for _date in dates:
            if not np.isnat(_date):
                date_time = self.to_datetime(_date)
                year = date_time.strftime("%Y")
                month = date_time.strftime("%m")
                day = date_time.strftime("%d")
                _time = date_time.strftime("%H:%M")
                self.date_time.append(day + "-" + month + "-" + year + "_" + _time)

        if self.date_time:
            self.cycle = self.date_time[0]

    def plot_sfc(self):
        """Plot only surface data"""
        pbar = tqdm(
            range(0, len(self.date_time)),
            desc="Plotting Variable : ",
            leave=False,
            colour="green",
        )
        pbar.write(
            "\n*** Initialising plotting for variable : "
            + utils.quote(self.var)
            + " ***\n"
        )
        data_plot = None
        for index in pbar:
            _time = self.date_time[index]
            if self.var == "slp":
                self.var_data = smooth2d(self.var_data, 3, cenweight=4)
                self.clevels = utils.get_auto_clevel(self.var_data, slp=True)
            else:
                self.clevels = json.loads(self.config.get(self.var, "clevels"))

            if data_plot is None:
                data_plot = self.var_data

            pbar.write("\tPlotting " + utils.quote(self.var) + " for Time: " + _time)
            pbar.set_description("Plotting " + utils.quote(self.var), refresh=True)
            self.plot_wrf_data(_time, index, data_plot=data_plot)
        tqdm.write(
            "\nPlotting of variable " + utils.quote(self.var) + " completed...\n"
        )

    def plot_upper(self):
        """Plot only upper atmospheric data"""
        pressure = getvar(self.nc_fh, "pressure", ALL_TIMES)
        self.clevels = json.loads(self.config.get(self.var, "clevels"))
        u_var_data = self.var_data
        if self.U is not None and self.V is not None:
            u_var_u_data = self.U
            u_var_v_data = self.V
        pbar_var = tqdm(
            range(0, len(self.date_time)),
            desc="Plotting Variable : ",
            leave=False,
            position=0,
            colour="green",
        )
        pbar_var.write(
            "\n*** Initialising plotting for variable : "
            + utils.quote(self.var)
            + " ***\n"
        )
        for index in pbar_var:
            _time = self.date_time[index]
            # Must initialise the bar inside time loop so that range is set every time entering into outer loop
            pbar_lvl = tqdm(
                self.ulevels,
                desc="Plotting Level : ",
                leave=False,
                position=1,
                colour="blue",
            )

            pbar_var.write(
                "\tPlotting " + utils.quote(self.var) + " for Time: " + _time
            )
            pbar_var.set_description("Overall Progress :", refresh=True)
            for self.ulevel in pbar_lvl:
                self.var_data = interplevel(u_var_data, pressure, self.ulevel)
                if self.U is not None and self.V is not None:
                    self.U = interplevel(u_var_u_data, pressure, self.ulevel)
                    self.V = interplevel(u_var_v_data, pressure, self.ulevel)
                tqdm.write("\t  at level" + utils.quote(self.ulevel))
                pbar_lvl.set_description("Plotting Level :", refresh=True)
                self.plot_wrf_data(_time=_time, index=index, data_plot=self.var_data, level=self.ulevel)
        tqdm.write("\nPlotting of " + utils.quote(self.var) + " completed...\n")

    def plot_wrf_data(self, _time, index, data_plot=None, level=None):
        """A wrapper function to call main plot method from plot class"""
        # For rainfall data we need to extract previous time data with current time data
        if self.var == "ppn":
            current = self.rainnc[index] + self.rainc[index]
            if index == 0:
                data_plot = current
            else:
                previous = self.rainnc[index - 1] + self.rainc[index - 1]
                data_plot = current - previous
        elif level is None:
            data_plot = data_plot[index]
        elif level is not None:
            data_plot = self.var_data[index]
        try:
            if self.U is not None and self.V is not None:
                plot_map = plot.MakePlot(
                    var_name=self.var,
                    data=self.convert_unit(data_plot),
                    u_kt=self.U[index],
                    v_kt=self.V[index],
                    lons=self.lons,
                    lats=self.lats,
                    u_level=self.ulevel,
                    run_time=self.cycle,
                    fcst_hr=_time,
                    proj=self.proj,
                    clevels=self.clevels,
                    output_dir=self.output,
                    dpi=self.dpi,
                    config_file=self.config,
                )
            else:
                plot_map = plot.MakePlot(
                    var_name=self.var,
                    data=self.convert_unit(data_plot),
                    lons=self.lons,
                    lats=self.lats,
                    u_level=self.ulevel,
                    run_time=self.cycle,
                    fcst_hr=_time,
                    proj=self.proj,
                    clevels=self.clevels,
                    output_dir=self.output,
                    dpi=self.dpi,
                    config_file=self.config,
                )
            plot_map.plot_var()
        except Exception as err:
            tqdm.write(str(err))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            tqdm.write(
                "\tError:"
                + str(err)
                + str(exc_type)
                + str(fname)
                + str(exc_tb.tb_lineno)
            )
            return False

    def convert_unit(self, data):
        """Convert data to other unit"""
        if self.var in ["T2", "u_temp", "u_theta", "u_tv", "u_twb"]:
            return convert.k_to_c(data)
        elif self.var in ["low_cloudfrac", "mid_cloudfrac", "high_cloudfrac"]:
            return np.round(data * 100)
        elif self.var == "winds":
            return convert.ms_to_kts(data)
        else:
            return data

    def list_projs(self):
        """List projection"""
        utils.list_proj()

    def get_title(self, var):
        """Get title from config file"""
        return json.loads(self.config.get(var, "title"))

    def get_unit(self):
        """Get unit from config file"""
        return self.config.get("theta_e", "unit")

    def get_proj(self):
        """Get projection details from data extracted"""
        if self.proj is None:
            self.proj = get_cartopy(self.var_data)


def _praser():
    """Form command line input"""
    prog_name = (
        "Command line application to plot static WRF model prognostic products..."
    )
    parser = argparse.ArgumentParser(
        description=prog_name, epilog="\u00a9 J Sundar, wrf.guy@gmail.com, 2022"
    )
    parser.add_argument(
        "--list-vars", action="store_true", help="List variables supported by wrfplot."
    )
    parser.add_argument(
        "--input",
        metavar="<input_file>",
        type=arguments.file_path,
        help="Mandatory path to WRF generated netCDF.",
    )
    parser.add_argument(
        "--output",
        metavar="<output_dir>",
        type=arguments.dir_path,
        default=False,
        help="Path to output directory for saving images.",
    )
    parser.add_argument(
        "--vars",
        metavar="<variable(s)>",
        type=arguments.validate_vars,
        help="Name of the variable to be plotted. Multiple variables are to be separated with"
        " ','. Use '--list-vars' option to see list of supported variables.",
    )
    parser.add_argument(
        "--dpi",
        metavar="<value>",
        type=int,
        help="Increase or decrease the plotted image resolution. Default is 125. More is higher resolution and"
        " less is course resolution. Higher values will reduce the speed of plot .",
    )
    parser.add_argument(
        "--list-cmaps",
        action="store_true",
        help="List colour maps (cmaps) supported by wrfplot.",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version information of application and exit.",
    )
    # args = parser.parse_args()
    return parser.parse_args()


def main():
    args = _praser()
    if args.list_vars:
        sys.exit(arguments.list_vars())
    elif args.list_cmaps:
        sys.exit(arguments.list_cmaps())
    elif args.version:
        sys.exit(print(__version__))
    elif not all([args.input, args.vars, args.output]):
        sys.exit(
            "You must provide path to WRF model output file using '--input' option, output directory for saving image files using '--output' option and must provide at least one variable name using '--var' option to process.\nTypical usage will be \"wrfplot --input filename' --output 'path/to/output/dir' --var 'slp'\""
        )
    elif all([args.input, args.vars, args.output]):
        file = fileio.FileIO(args.input)
        if file.is_wrf():
            wrfplt = Wrfplot(
                input_path=args.input, output_path=args.output, dpi=args.dpi
            )
            try:
                wrfplt.read_file(args.input)
                if isinstance(args.vars, list):
                    for var in args.vars:
                        wrfplt.read_data(var)
                        wrfplt.read_latlons()
                        wrfplt.get_proj()
                        wrfplt.plot_variables()  
                else:  
                    wrfplt.read_data(args.vars)
                    wrfplt.read_latlons()
                    wrfplt.get_proj()
                    wrfplt.plot_variables()
                print("Plotting process completed...\n")
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                print("Failed to plot one or some variables...")


if __name__ == "__main__":
    main()
